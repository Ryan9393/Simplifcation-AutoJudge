from prompt.prompt_builder import create_full_prompt

NAME = "full"
REQUEST_KIND = "raw"
TEMPERATURE = 0
RATE_LIMIT = 100


async def score(ask_once, request, response) -> float:
    result = await ask_once(create_full_prompt(request, response))
    return float(result)
