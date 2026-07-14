import pathlib
from dataclasses import dataclass
from typing import List, Optional

ROOT = pathlib.Path(__file__).resolve().parent


@dataclass
class SourceConfig:
    name: str
    id_field: str  # attribute shared by request/checklist objects and Response.metadata
    raw_request_path: pathlib.Path
    response_base_path: pathlib.Path
    checklist_path: pathlib.Path
    checklist_as_list_path: Optional[pathlib.Path]
    output_format: str  # passed to Leaderboard.write(format=...)


SOURCES = {
    "ragtime": SourceConfig(
        name="ragtime",
        id_field="request_id",
        raw_request_path=ROOT / "ragtime25_main_all.jsonl",
        response_base_path=ROOT / "ragtime-export" / "runs" / "repgen",
        checklist_path=ROOT / "checklists" / "ragtime.checklist.jsonl",
        checklist_as_list_path=ROOT / "checklists" / "ragtime.checklist_as_list.jsonl",
        output_format="ir_measures",
    ),
    "rag4reports": SourceConfig(
        name="rag4reports",
        id_field="topic_id",
        raw_request_path=ROOT / "rag4reports" / "data" / "report-requests.jsonl",
        response_base_path=ROOT / "rag4reports" / "data" / "generated-reports",
        checklist_path=ROOT / "checklists" / "rag4reports.checklist.jsonl",
        checklist_as_list_path=ROOT / "checklists" / "rag4reports.checklist_as_list.jsonl",
        output_format="rag4reports",
    ),
}


def discover_runs(source: SourceConfig) -> List[str]:
    return sorted(p.name for p in source.response_base_path.iterdir() if p.is_file())


def get_response_for(entity_id, responses, source: SourceConfig):
    for resp in responses:
        if resp.metadata is not None and str(getattr(resp.metadata, source.id_field)) == str(entity_id):
            return resp
    return None
