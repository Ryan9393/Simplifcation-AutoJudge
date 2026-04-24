#CHECK HOW MANY RUNS FIRST BEFORE RUNNING PLEASE PLEASE PLEASE
import os
import asyncio
import pathlib
from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from data.json_loader import load_checklists_as_list, load_responses, get_response_for_request
from prompt.prompt_builder import create_single_checklist_item_prompt
from autojudge_base import LeaderboardBuilder, LeaderboardSpec, MeasureSpec


load_dotenv(dotenv_path=".env/autojudge.env")

#None means full file
k = None

MAX_ATTEMPTS = 3
#Change limiter
limiter = AsyncLimiter(max_rate=100, time_period=60)

request_path = pathlib.Path(__file__).resolve().parent / "checklists_as_lists.jsonl"
response_path_base = pathlib.Path(__file__).resolve().parent.parent / "ragtime-export/runs/repgen"

RESPONSE_RUNS = [
    "aloe", "anise", "ant", "beet", "berry", "boar", "camel", "carp", "cat", "chili",
    "cod", "colt", "crab", "deer", "dill", "dog", "eel", "elk", "emu", "ewe",
    "fig", "fly", "frog", "gar", "gull", "guppy", "hen", "lichen", "loon", "mango",
    "maple", "melon", "mink", "mite", "mole", "moss", "moth", "nut", "oats", "okra",
    "olive", "onion", "perch", "plum", "poppy", "radish", "rat", "rose", "rye", "skink",
    "skunk", "squid", "swan", "tern", "tick", "toad", "trout", "ulva", "yak", "yam", "yew",
]

response_paths = [response_path_base / run for run in RESPONSE_RUNS]

FULL_DATA = LeaderboardSpec(measures=(MeasureSpec("RELEVANCE"),))


async def async_generate(response_path: pathlib.Path, builder: LeaderboardBuilder, processed_topic_ids: list):
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    requests = load_checklists_as_list(request_path)
    responses = load_responses(response_path)

    if k is not None:
        requests_to_process = requests[:k]
    else:
        requests_to_process = requests

    async def ask_once(prompt: str) -> str:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            async with limiter:
                try:
                    resp = await client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
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

        total_score = 0

        for item in request.checklist:
            prompt = create_single_checklist_item_prompt(item, response)

            try:
                raw_score = await ask_once(prompt)
            except Exception as e:
                print(f"Failed scoring {request.request_id} item: {e}")
                continue

            try:
                numeric_score = float(raw_score)
            except ValueError:
                print(f"Non-numeric score '{raw_score}', treating as 0")
                numeric_score = 0

            total_score += numeric_score

        builder.add(
            run_id=response.metadata.run_id,
            topic_id=str(request.request_id),
            values={
                "RELEVANCE": total_score
            },
        )

        processed_topic_ids.append(request.request_id)
        print(f"Processed {request.request_id} with total score {total_score}")


async def main():
    builder = LeaderboardBuilder(FULL_DATA)
    processed_topic_ids = []

    for run in RESPONSE_RUNS:
        path = response_path_base / run
        print(f"Running evaluation for: {run}")
        await async_generate(path, builder, processed_topic_ids)

    leaderboard = builder.build(
        expected_topic_ids=processed_topic_ids,
        on_missing="fix_aggregate"
    )

    leaderboard.write(pathlib.Path("Checklist_as_list.output.eval.txt"), format="ir_measures")

if __name__ == "__main__":
    asyncio.run(main())