from prompt.prompt_builder import create_single_checklist_item_prompt

NAME = "checklist_as_list"
REQUEST_KIND = "checklist_as_list"
TEMPERATURE = 0.5
RATE_LIMIT = 100


async def score(ask_once, request, response) -> float:
    total = 0.0
    for item in request.checklist:
        raw = await ask_once(create_single_checklist_item_prompt(item, response))
        try:
            total += float(raw)
        except ValueError:
            print(f"Non-numeric score '{raw}', treating as 0")
    return total
