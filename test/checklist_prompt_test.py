import pathlib
from data.json_loader import load_checklists, load_responses, get_response_for_request_rag4reports
from prompt.prompt_builder import create_checklist_prompt

request_path = pathlib.Path(__file__).resolve().parent.parent / "rag4reports_methods/rag4reports_checklists.jsonl"
response_path = pathlib.Path(__file__).resolve().parent.parent / "rag4reports/data/generated-reports/adventure-continue"
OUTPUT_FILE = pathlib.Path("checklist_prompt_preview.txt")


def main():
    requests = load_checklists(request_path)
    responses = load_responses(response_path)

    if not requests:
        print("No requests found.")
        return

    request = requests[0]
    response = get_response_for_request_rag4reports(request.topic_id, responses)

    if response is None:
        print("No matching response found.")
        return
    

    rendered_prompt = create_checklist_prompt(request, response)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rendered_prompt)

    print(f"Prompt written to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
