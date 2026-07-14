import argparse
import asyncio
import json

from aiolimiter import AsyncLimiter

from data.json_loader import load_requests
from judge.io_utils import confirm_reuse
from judge.llm_client import make_asker, make_client
from prompt.prompt_builder import create_checklist_builder_prompt
from sources import SOURCES

RATE_LIMIT = 100
TEMPERATURE = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a checklist file for a source.")
    parser.add_argument("--source", choices=sorted(SOURCES), required=True)
    return parser.parse_args()


async def build_checklists(source_name: str) -> None:
    source = SOURCES[source_name]
    output_path = source.checklist_path

    if output_path.exists() and confirm_reuse(output_path, "Checklist file"):
        print(f"Using existing checklist file at {output_path}")
        return

    requests = load_requests(source.raw_request_path)
    if not requests:
        print("No requests found.")
        return

    client = make_client()
    limiter = AsyncLimiter(max_rate=RATE_LIMIT, time_period=60)
    ask_once = make_asker(client, limiter, TEMPERATURE)

    results = []
    for i, request in enumerate(requests):
        entity_id = getattr(request, source.id_field)
        print(f"Processing request {i + 1}/{len(requests)} (ID={entity_id})")

        output = await ask_once(create_checklist_builder_prompt(request))
        results.append({source.id_field: str(entity_id), "checklist": output})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item) + "\n")

    print(f"Saved {len(results)} checklists to {output_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(build_checklists(parse_args().source))
