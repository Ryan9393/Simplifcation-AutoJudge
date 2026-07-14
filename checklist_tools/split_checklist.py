import argparse
import json
import re
from typing import List

from data.json_loader import load_checklists
from judge.io_utils import confirm_reuse
from sources import SOURCES

ITEM_PATTERN = re.compile(r"(?m)^\s*\d+\.\s+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a flat numbered checklist file into a checklist_as_list file."
    )
    parser.add_argument("--source", choices=sorted(SOURCES), required=True)
    return parser.parse_args()


def split_checklist_text(checklist: str) -> List[str]:
    return [item.strip() for item in ITEM_PATTERN.split(checklist) if item.strip()]


def split_checklists(source_name: str) -> None:
    source = SOURCES[source_name]
    if source.checklist_as_list_path is None:
        raise SystemExit(f"Source '{source_name}' has no checklist_as_list_path configured.")

    output_path = source.checklist_as_list_path
    if output_path.exists() and confirm_reuse(output_path, "Checklist-as-list file"):
        print(f"Using existing checklist_as_list file at {output_path}")
        return

    if not source.checklist_path.exists():
        raise SystemExit(
            f"No checklist file at {source.checklist_path}. "
            f"Run: python -m checklist_tools.build_checklists --source {source_name}"
        )

    checklists = load_checklists(source.checklist_path)

    results = []
    for checklist in checklists:
        entity_id = getattr(checklist, source.id_field)
        results.append({
            source.id_field: str(entity_id),
            "checklist": split_checklist_text(checklist.checklist),
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item) + "\n")

    print(f"Saved {len(results)} checklist_as_list entries to {output_path.resolve()}")


if __name__ == "__main__":
    split_checklists(parse_args().source)
