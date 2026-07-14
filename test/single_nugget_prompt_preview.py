import pathlib
from data.json_loader import load_requests, load_responses
from prompt.prompt_builder import create_single_nugget_prompt
from sources import SOURCES, get_response_for

source = SOURCES["ragtime"]
response_path = source.response_base_path / "aloe"
OUTPUT_FILE = pathlib.Path("single_nugget_prompt_preview.txt")


def main():
    requests = load_requests(source.raw_request_path)
    responses = load_responses(response_path)

    if not requests:
        print("No requests found.")
        return

    request = requests[1]
    response = get_response_for(request.request_id, responses, source)

    if response is None:
        print("No matching response found.")
        return

    prompts = []

    for i, item in enumerate(response.responses):
        nugget_text = item.text.strip()

        if not nugget_text or len(nugget_text) < 15:
            continue

        prompt = create_single_nugget_prompt(request, nugget_text)

        prompts.append(f"===== NUGGET {i+1} =====\n{prompt.strip()}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(prompts))

    print(f"{len(prompts)} prompts written to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()