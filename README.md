# Simplification-AutoJudge

Simplification-based AutoJudge for the TREC AutoJudge / RAG4Reports tasks. Uses LLMs to automatically score RAG system outputs, ranking which systems generate the most human liked response.

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
