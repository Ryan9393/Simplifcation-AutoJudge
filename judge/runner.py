import pathlib
from typing import Optional

from aiolimiter import AsyncLimiter
from autojudge_base import LeaderboardBuilder, LeaderboardSpec, MeasureSpec

from data.json_loader import (
    load_checklists,
    load_checklists_as_list,
    load_requests,
    load_responses,
)
from judge.llm_client import make_asker, make_client
from sources import SourceConfig, discover_runs, get_response_for

LEADERBOARD_DIR = pathlib.Path(__file__).resolve().parent.parent / "leaderboards"

_REQUEST_LOADERS = {
    "raw": lambda source: load_requests(source.raw_request_path),
    "checklist": lambda source: load_checklists(source.checklist_path),
    "checklist_as_list": lambda source: load_checklists_as_list(source.checklist_as_list_path),
}


def _require_checklist_file(source: SourceConfig, method) -> None:
    if method.REQUEST_KIND == "checklist" and not source.checklist_path.exists():
        raise FileNotFoundError(
            f"No checklist file at {source.checklist_path}. "
            f"Run: python -m checklist_tools.build_checklists --source {source.name}"
        )
    if method.REQUEST_KIND == "checklist_as_list":
        if source.checklist_as_list_path is None:
            raise ValueError(f"Source '{source.name}' has no checklist_as_list data.")
        if not source.checklist_as_list_path.exists():
            raise FileNotFoundError(f"No checklist_as_list file at {source.checklist_as_list_path}.")


async def run_leaderboard(source: SourceConfig, method, k: Optional[int] = None) -> pathlib.Path:
    _require_checklist_file(source, method)

    requests = _REQUEST_LOADERS[method.REQUEST_KIND](source)
    if k is not None:
        requests = requests[:k]

    client = make_client()
    limiter = AsyncLimiter(max_rate=method.RATE_LIMIT, time_period=60)
    ask_once = make_asker(client, limiter, method.TEMPERATURE)

    builder = LeaderboardBuilder(LeaderboardSpec(measures=(MeasureSpec("RELEVANCE"),)))
    processed_topic_ids = []

    for run in discover_runs(source):
        print(f"Running evaluation for: {run}")
        responses = load_responses(source.response_base_path / run)

        for request in requests:
            entity_id = getattr(request, source.id_field)
            response = get_response_for(entity_id, responses, source)

            if response is None:
                print(f"No matching response found for {entity_id}. Skipping.")
                continue

            try:
                score = await method.score(ask_once, request, response)
            except Exception as e:
                print(f"Failed scoring {entity_id}: {e}")
                continue

            builder.add(
                run_id=response.metadata.run_id,
                topic_id=str(entity_id),
                values={"RELEVANCE": score},
            )
            processed_topic_ids.append(entity_id)
            print(f"Processed {entity_id}")

    leaderboard = builder.build(
        expected_topic_ids=processed_topic_ids,
        on_missing="fix_aggregate",
    )

    LEADERBOARD_DIR.mkdir(exist_ok=True)
    output_path = LEADERBOARD_DIR / f"{method.NAME}.{source.name}.output.eval.txt"
    leaderboard.write(output_path, format=source.output_format)
    return output_path
