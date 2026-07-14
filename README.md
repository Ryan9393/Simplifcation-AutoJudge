# Simplification-AutoJudge

Simplification-based AutoJudge for the TREC AutoJudge / RAG4Reports tasks. Uses LLMs to automatically score RAG system outputs, ranking which systems generate the most human liked response.

## Setup

```bash
pip install -r requirements.txt
```

Add an OpenRouter API key to `.env/autojudge.env`:

```
OPENROUTER_API_KEY=...
```

## Scoring methods

Each method in `methods/` pairs a prompt with a scoring strategy:

- `full` — one-shot relevance score (0-3) against the whole response.
- `checklist` — one-shot score against a generated checklist.
- `checklist_as_list` — scores each checklist item individually and sums them.
- `nuggets` — one-shot average relevance across all response nuggets.
- `single_nugget` — scores each nugget individually and averages them.

## Usage

`checklist` needs a checklist file first. Build one with:

```bash
python -m checklist_tools.build_checklists --source ragtime
```

`checklist_as_list` needs that same checklist split into individual items. Derive it with:

```bash
python -m checklist_tools.split_checklist --source ragtime
```

Both scripts ask whether to reuse or regenerate if their output file already exists.

Then run a leaderboard for any source/method combination:

```bash
python run.py --source ragtime --method checklist
python run.py --source rag4reports --method full --k 5   # --k limits to the first K requests, for a quick test run
```

Results are written to `leaderboards/{method}.{source}.output.eval.txt`.

Prompt previews for manual inspection live in `test/` (e.g. `python -m test.nugget_prompt_preview`).
