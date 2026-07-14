from prompt.prompt_builder import create_single_nugget_prompt

NAME = "single_nugget"
REQUEST_KIND = "raw"
TEMPERATURE = 0
RATE_LIMIT = 300
MIN_NUGGET_LENGTH = 15


async def score(ask_once, request, response) -> float:
    scores = []
    for item in response.responses:
        nugget_text = item.text.strip()
        if not nugget_text or len(nugget_text) < MIN_NUGGET_LENGTH:
            continue

        raw = await ask_once(create_single_nugget_prompt(request, nugget_text))
        try:
            scores.append(int(raw))
        except ValueError:
            print(f"Non-numeric nugget score '{raw}', skipping")

    return sum(scores) / len(scores) if scores else 0.0
