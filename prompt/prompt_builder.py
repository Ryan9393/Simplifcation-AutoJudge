def create_full_prompt(request, response) -> str:
    request_text = f"""Title: {request.title}

Background:
{request.background}

Problem:
{request.problem_statement}
"""

    response_text = "\n".join(r.text for r in response.responses)

    return f"""
You are evaluating how relevant a document is to a report request.

Use the following grading rubric:

3 Fully Relevant:
The response directly addresses the core requirements of the request and covers the major requested aspects in a substantive way.

2 Mostly Relevant:
The response addresses the main topic and some key aspects but is incomplete or missing important elements.

1 Slightly Relevant:
The response relates to the general topic but does not meaningfully address the specific requirements.

0 Not Relevant:
The response does not address the request or is unrelated.

Request:
{request_text}

Response:
{response_text}

Return ONLY one number: 3, 2, 1, or 0.
Do not explain your answer.
"""
