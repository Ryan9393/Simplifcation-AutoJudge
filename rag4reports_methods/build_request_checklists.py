import os
import asyncio
import pathlib
import json
from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter

from data.json_loader import load_requests
from prompt.prompt_builder import create_checklist_builder_prompt

load_dotenv(dotenv_path=".env/autojudge.env")

MAX_ATTEMPTS = 3
limiter = AsyncLimiter(max_rate=100, time_period=60)

request_path = pathlib.Path(__file__).resolve().parent / "ragtime25_main_all.jsonl"
OUTPUT_FILE = pathlib.Path("checklists.json")


async def async_generate_checklists():
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    requests = load_requests(request_path)

    if not requests:
        print("No requests found.")
        return

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
                        print(f"Error {e}. Retrying...")
                        await asyncio.sleep(5)
                    else:
                        print(f"Error {e}. Giving up.")
                        raise

    results = []

    for i, request in enumerate(requests):
        print(f"Processing request {i+1}/{len(requests)} (ID={request.topic_id})")

        prompt = create_checklist_builder_prompt(request)

        output = await ask_once(prompt)

        results.append({
            "topic_id": str(request.topic_id),
            "checklist": output
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved {len(results)} checklists to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    asyncio.run(async_generate_checklists())