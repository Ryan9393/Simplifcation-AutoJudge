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


def create_checklist_prompt(checklist_request, response) -> str:
    response_text = "\n".join(r.text for r in response.responses)

    return f"""
You are evaluating how well a response satisfies a checklist.

Checklist:
{checklist_request}

Response:
{response_text}

Instructions:
- Each checklist item is worth 1 point.
- Award 1 point if the response clearly satisfies the item.
- Award 0 points if it does not.
- Be strict: partial or vague matches do NOT count.
- Sum the total points.

Return ONLY the total score as a number.
Do not explain your answer.
"""


def create_checklist_builder_prompt(request, num_items: int = 5) -> str:
    request_text = f"""Title: {request.title}

Background:
{request.background}

Problem:
{request.problem_statement}
"""

    return f"""
You are generating a checklist to evaluate how well a response satisfies a report request.

Request:
{request_text}

Instructions:
- Create EXACTLY {num_items} checklist items.
- Each item must represent ONE distinct requirement.
- Items must be specific, objective, and clearly checkable.
- Avoid overlap between items.
- Cover the most important aspects of the request.
- If needed, merge or prioritize less important details to stay within {num_items} items.
- Ensure a balanced checklist (not all items about the same aspect).

Output format:
- Return a numbered list (1., 2., 3., ...).
- Each item must be a single sentence.
- Do NOT include explanations or extra text.

Return ONLY the checklist.
"""
