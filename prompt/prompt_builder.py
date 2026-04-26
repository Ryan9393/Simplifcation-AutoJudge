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
{checklist_request.checklist}

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



def create_nugget_prompt(request, response) -> str:
    request_text = f"""Title: {request.title}

Background:
{request.background}

Problem:
{request.problem_statement}
"""

    nuggets = [
        f"[NUGGET {i+1}]:\n {item.text.strip()}"
        for i, item in enumerate(response.responses)
        if item.text.strip()
    ]

    nuggets_text = "\n".join(nuggets)

    return f"""
You are evaluating how relevant individual response nuggets are to a report request.

Each nugget should be graded independently using this rubric:

1 Relevant:
The nugget meaningfully contributes to addressing the request.

0 Not Relevant:
The nugget does not help address the request or is off-topic.

Instructions:
- Assign a score (0 or 1) to EACH nugget.
- Then compute the average score across all nuggets.
- Return ONLY the final average as a decimal between 0 and 1.
- Do NOT include explanations.
- Do NOT list individual scores.

Request:
{request_text}

Response Nuggets:
{nuggets_text}

Return ONLY the average score (e.g., 0.0, 0.5, 1.0).
"""


def create_single_checklist_item_prompt(checklist_item: str, response) -> str:
    response_text = "\n".join(r.text for r in response.responses)

    return f"""
You are evaluating whether a response satisfies a single requirement.

requirement:
{checklist_item}

Response:
{response_text}

Instructions:
- Return 1 if the response clearly and explicitly satisfies the requirement.
- Return 0 if it does not.
- Be strict: partial, vague, or implied matches do NOT count.
- Do not infer intent—only count what is directly supported by the text.

Return ONLY a single number: 0 or 1.
Do not explain your answer.
"""


def create_single_nugget_prompt(request, nugget_text: str) -> str:
    request_text = f"""Title: {request.title}

Background:
{request.background}

Problem:
{request.problem_statement}
"""

    return f"""
You are evaluating how relevant a response nugget is to a report request.

Scoring rubric:

1 Relevant:
The nugget meaningfully contributes to addressing the request.

0 Not Relevant:
The nugget does not help address the request or is off-topic.

Instructions:
- Assign a score of 0 or 1.
- Return ONLY the score.
- Do NOT include explanations.

Request:
{request_text}

Nugget:
{nugget_text.strip()}

Return ONLY 0 or 1.
"""