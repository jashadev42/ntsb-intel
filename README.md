# aviation-incident-intel

An NLP pipeline that ingests, classifies, and semantically searches NTSB
aviation incident reports — turning thousands of inconsistent, narrative-heavy
government documents into a searchable system that answers plain-English
questions with citations to specific reports.

> **Status:** In active development. Ingest stage complete (full dataset loads
> into a queryable SQLite database). Classification stage next. See
> [Roadmap](#roadmap) for current scope.

## The problem

The NTSB publishes thousands of aviation incident and accident reports. They
are long, inconsistently structured, and difficult to search — there is no good
way to ask a question like *"show me incidents involving fuel system failures in
small aircraft since 2020"* and get a grounded, cited answer. This project builds
the tool that makes that question answerable.

## Architecture

```mermaid
flowchart TD
    A[NTSB public data<br/>raw incident reports] --> B[1. Ingest<br/>parse & clean JSON,<br/>store in SQLite]
    B --> C[2. Classify<br/>fine-tuned DistilBERT tags each report<br/>by probable-cause category]
    C --> D[3. Index<br/>embed report text,<br/>load into FAISS vector store]
    D --> E[4. Serve<br/>FastAPI endpoint: retrieve relevant<br/>reports + generate grounded answer]
    E --> F[Grounded answer<br/>with citations to specific reports]
```

Each stage's output is the next stage's input, so the stages are independently
testable: ingest produces a clean database, classify adds labels to it, index
builds a vector store from it, and serve reads what's already there.

## Tech stack

**In use:** Python 3.12+, uv, pytest, Git, SQLite, json/sqlite3 (stdlib)
**Planned:** PyTorch, HuggingFace Transformers (DistilBERT), scikit-learn,
sentence-transformers, FAISS, FastAPI, Docker

## Roadmap

- [x] Project scaffolding and packaging (uv, src layout)
- [x] **Ingest** — pull NTSB reports, clean with pandas, store in SQLite
- [ ] **Classify** — fine-tune DistilBERT to tag reports by probable-cause category
- [ ] **Index** — embed reports into a FAISS vector store
- [ ] **Serve** — FastAPI RAG endpoint returning grounded, cited answers
- [ ] **Package** — Dockerize, single-command `docker-compose up`

## Setup

```bash
uv sync
```

**Get the data:** Download the aviation dataset as JSON from the
[NTSB CAROL query builder](https://data.ntsb.gov/carol-main-public/query-builder)
(filter to Aviation, event date 2020 onward, then use **Download Data (JSON)**).
Save it to `data/aviation_raw.json`.

**Run ingest:**

```bash
uv run python -m ntsb_intel.ingest
```

This loads ~10,000 incident reports into a local SQLite database at
`data/incidents.db`.

_(Requires [uv](https://docs.astral.sh/uv/). Keep the project in a path without spaces.)_