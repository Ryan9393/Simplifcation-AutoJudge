import json
import pathlib

INPUT_FILE = pathlib.Path("checklists.json")
OUTPUT_FILE = pathlib.Path("checklists.jsonl")


def convert_json_to_jsonl(input_path: pathlib.Path, output_path: pathlib.Path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

    print(f"Converted {len(data)} items to {output_path.resolve()}")


if __name__ == "__main__":
    convert_json_to_jsonl(INPUT_FILE, OUTPUT_FILE)