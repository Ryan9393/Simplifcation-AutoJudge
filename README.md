# Simplification-AutoJudge

Simplification-based AutoJudge for the TREC AutoJudge / RAG4Reports tasks. Uses LLMs to automatically score RAG system outputs against nugget checklists, returning a binary vector indicating which nuggets are covered by an answer — e.g. `[0, 0, 1, 0, 1]`.

## Setup

```bash
pip install autojudge-base
```

## Usage

```bash
# Preview a nugget prompt
py -3.13 -m test.nugget_prompt_preview

# Build RAG4Reports request checklists
py -3.13 -m rag4reports_methods.build_request_checklists
```