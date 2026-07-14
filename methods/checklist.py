from prompt.prompt_builder import create_checklist_prompt

NAME = "checklist"
REQUEST_KIND = "checklist"
TEMPERATURE = 0
RATE_LIMIT = 100


async def score(ask_once, request, response) -> float:
    result = await ask_once(create_checklist_prompt(request, response))
    return float(result)
