import pathlib
from data.json_loader import load_requests
from prompt.prompt_builder import create_checklist_builder_prompt

request_path = pathlib.Path(__file__).resolve().parent.parent / "rag4reports/data/report-requests.jsonl"
OUTPUT_FILE = pathlib.Path("checklist_builder_prompt_preview.txt")


def main():
    requests = load_requests(request_path)

    if not requests:
        print("No requests found.")
        return

    request = requests[2]

    rendered_prompt = create_checklist_builder_prompt(request)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rendered_prompt)

    print(f"Checklist builder prompt written to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()