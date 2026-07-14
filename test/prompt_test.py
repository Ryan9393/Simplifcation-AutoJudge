import pathlib
from data.json_loader import load_requests, load_responses
from prompt.prompt_builder import create_full_prompt
from sources import SOURCES, get_response_for

source = SOURCES["ragtime"]
response_path = source.response_base_path / "aloe"
OUTPUT_FILE = pathlib.Path("llm_prompt_preview.txt")


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

    rendered_prompt = create_full_prompt(request, response)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rendered_prompt)

    print(f"Prompt written to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()

