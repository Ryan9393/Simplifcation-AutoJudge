import pathlib
from typing import List
from models.request import Request
from models.response import Response
from models.request_checklist import Request_Checklist
from models.request_checklist_as_list import Request_Checklist_As_List

def load_requests(file_path: pathlib.Path) -> List[Request]:
    requests = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                requests.append(Request.model_validate_json(line.strip()))
            except Exception as e:
                print(f"Error parsing request: {e}")
    return requests

def load_responses(file_path: pathlib.Path) -> List[Response]:
    responses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                responses.append(Response.model_validate_json(line.strip()))
            except Exception as e:
                print(f"Error parsing response: {e}")
    return responses

def load_checklists(path: pathlib.Path) -> List[Request_Checklist]:
    checklists = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            checklists.append(Request_Checklist.model_validate_json(line.strip()))
    return checklists

def load_checklists_as_list(path: pathlib.Path) -> List[Request_Checklist_As_List]:
    checklists = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            checklists.append(Request_Checklist_As_List.model_validate_json(line.strip()))
    return checklists