import asyncio
import os
from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter

load_dotenv(dotenv_path=".env/autojudge.env")

MAX_ATTEMPTS = 3
REQUEST_TIMEOUT = 60


def make_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )


def make_asker(client: AsyncOpenAI, limiter: AsyncLimiter, temperature: float):
    async def ask_once(prompt: str) -> str:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            async with limiter:
                try:
                    resp = await asyncio.wait_for(
                        client.chat.completions.create(
                            model="openai/gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature,
                        ),
                        timeout=REQUEST_TIMEOUT,
                    )
                    return resp.choices[0].message.content.strip()

                except OpenAIError as e:
                    if attempt < MAX_ATTEMPTS:
                        print(f"Error {e}. Retrying ({attempt}/{MAX_ATTEMPTS})...")
                        await asyncio.sleep(5)
                    else:
                        print(f"Error {e}. Giving up.")
                        raise

    return ask_once
