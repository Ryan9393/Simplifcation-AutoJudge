import os
import asyncio
import pathlib
from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from data.json_loader import load_requests, load_responses, get_response_for_request
from prompt.prompt_builder import create_full_prompt
from autojudge_base import LeaderboardBuilder, LeaderboardSpec, MeasureSpec

load_dotenv(dotenv_path=".env/autojudge.env")

MAX_ATTEMPTS = 3
limiter = AsyncLimiter(max_rate=10, time_period=60)

request_path = pathlib.Path(__file__).resolve().parent / "ragtime25_main_all.jsonl"
response_path = pathlib.Path(__file__).resolve().parent / "ragtime-export/runs/repgen/aloe"

FULL = LeaderboardSpec(measures=(MeasureSpec("RELEVANCE"),))


async def async_generate():

    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    requests = load_requests(request_path)
    responses = load_responses(response_path)

    if not requests:
        print("No requests found.")
        return

    request = requests[0]

    response = get_response_for_request(request.request_id, responses)

    if response is None:
        print("No matching response found.")
        return

    prompt = create_full_prompt(request, response)

    async def ask_once(prompt: str) -> str:

        for attempt in range(1, MAX_ATTEMPTS + 1):
            async with limiter:
                try:
                    resp = await client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0,
                    )
                    print(resp)
                    return resp.choices[0].message.content.strip()

                except OpenAIError as e:
                    if attempt < MAX_ATTEMPTS:
                        print(f"Error {e}. Retrying...")
                        await asyncio.sleep(5)
                    else:
                        print(f"Error {e}. Giving up.")
                        raise

    score = await ask_once(prompt)

    builder = LeaderboardBuilder(FULL)

    builder.add(
        run_id=response.metadata.run_id,
        topic_id=str(request.request_id),
        values={
            "RELEVANCE": score
        },  
    )

    leaderboard = builder.build(
        expected_topic_ids=[request.request_id],
        on_missing="fix_aggregate"
    )

    print(leaderboard)
    leaderboard.write(pathlib.Path("output.eval"), format="ir_measures")


if __name__ == "__main__":
    asyncio.run(async_generate())
