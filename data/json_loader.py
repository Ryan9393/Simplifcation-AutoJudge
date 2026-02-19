import pathlib
from typing import List
from models.request import Request
from models.response import Response

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

def get_response_for_request(request_id: int, responses: List[Response]):
    for resp in responses:
        if str(resp.metadata.request_id) == str(request_id):
            return resp
    return None