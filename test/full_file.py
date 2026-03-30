#CHECK HOW MANY RUNS FIRST BEFORE RUNNING PLEASE PLEASE PLEASE
import os
import asyncio
import pathlib
from typing import Optional
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
# request_path = pathlib.Path(__file__).resolve().parent / "kiddie/runs/repgen/run1.jsonl"
# response_path = pathlib.Path(__file__).resolve().parent / "kiddie/topics/kiddie-topics.jsonl"
#List of response paths
#aloe anise ant beet berry boar camel carp cat chili cod colt crab deer dill dog ell elk emu ewe fig fly frog gar gull guppy
#hen lichen loon mango maple melon mink mite mole moss moth nut oats okra olive onion perch plum poppy radish rat rose rye skink
#skunk squid swan tern tick toad trout ulva yak yam yew

FULL_DATA = LeaderboardSpec(measures=(MeasureSpec("RELEVANCE"),))


async def async_generate(k: Optional[int] = None):
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    requests = load_requests(request_path)
    responses = load_responses(response_path)

    if k is not None:
        requests_to_process = requests[:k]
    else:
        requests_to_process = requests

    builder = LeaderboardBuilder(FULL_DATA)
    processed_topic_ids = []

    async def ask_once(prompt: str) -> str:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            async with limiter:
                try:
                    resp = await client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0,
                    )
                    return resp.choices[0].message.content.strip()

                except OpenAIError as e:
                    if attempt < MAX_ATTEMPTS:
                        print(f"Error {e}. Retrying ({attempt}/{MAX_ATTEMPTS})...")
                        await asyncio.sleep(5)
                    else:
                        print(f"Error {e}. Giving up.")
                        raise

    for request in requests_to_process:
        response = get_response_for_request(request.request_id, responses)

        if response is None:
            print(f"No matching response found for {request.request_id}. Skipping.")
            continue

        prompt = create_full_prompt(request, response)

        try:
            score = await ask_once(prompt)
        except Exception as e:
            print(f"Failed scoring {request.request_id}: {e}")
            continue

        builder.add(
            run_id=response.metadata.run_id,
            topic_id=str(request.request_id),
            values={
                "RELEVANCE": score
            },
        )

        processed_topic_ids.append(request.request_id)
        #print(f"Processed {request.request_id}")


    leaderboard = builder.build(
        expected_topic_ids=processed_topic_ids,
        on_missing="fix_aggregate"
    )

    #print(leaderboard)
    leaderboard.write(pathlib.Path("output.eval"), format="ir_measures")


if __name__ == "__main__":
    #None means full file
    asyncio.run(async_generate(k=None))