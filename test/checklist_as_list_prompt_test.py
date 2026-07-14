import pathlib
from data.json_loader import load_checklists_as_list, load_responses
from prompt.prompt_builder import create_single_checklist_item_prompt
from sources import SOURCES, get_response_for

source = SOURCES["ragtime"]
response_path = source.response_base_path / "aloe"
OUTPUT_FILE = pathlib.Path("checklist_as_list_prompt_preview.txt")


def main():
    requests = load_checklists_as_list(source.checklist_as_list_path)
    responses = load_responses(response_path)

    if not requests:
        print("No requests found.")
        return

    request = requests[0]
    response = get_response_for(request.request_id, responses, source)

    if response is None:
        print("No matching response found.")
        return
    

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in request.checklist:
            prompt = create_single_checklist_item_prompt(item, response)
            f.write(prompt)
            f.write("\n\n" + "="*80 + "\n\n")

    print(f"Prompt written to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()