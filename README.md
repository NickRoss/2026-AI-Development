# 2026-AI-Development
Winter 2026 AI Development Training Series

This course was developed in partnership between the University of Chicago's [Career Advancement Office](https://careeradvancement.uchicago.edu/) and the University of Chicago's [Data Science Institute](https://datascience.uchicago.edu/).

**The work below is incomplete -- the final course will be coming soon!**


## Workshop: AI Development (4-part series)

This repository contains materials for a four-part workshop on AI development for advanced undergraduates (3rd/4th year).

### Lecture 1 (slides-first)
- **Topic**: LLMs, agents, tools, and MCP concepts (plus costing/MLOps discussion)
- **Slides**: `lecture_1/slides/lecture_1.tex`

> Lecture 1 content is adapted from Nick Ross's course notes on LLMs/agents/MCP: `https://raw.githubusercontent.com/NickRoss/2025-Data-24100/main/class_notes/16_llms_agents_mcp.md`

### Lecture 2 (HITL + evaluation)
- **Problem**: Marketing automation / outreach drafting with compliance
- **Notebook**: `lecture_2/notebooks/lecture_2_marketing_hitl.ipynb`
- **Data/docs**: `lecture_2/data/` (leads + brand + product one-pager + rubric)

### Lecture 3 (grounding + API actions)
- **Problem**: Support ticket triage with grounded replies and safe external actions
- **Notebook**: `lecture_3/notebooks/lecture_3_support_triage_api.ipynb`
- **Data/docs**: `lecture_3/data/` (tickets + KB + stub API data)

### Lecture 4 (tools/MCP-like + orchestrator)
- **Problem**: Research brief generation using a tool registry and a simple orchestrator loop
- **Notebook**: `lecture_4/notebooks/lecture_4_tooling_orchestrator.ipynb`
- **Data/docs**: `lecture_4/data/` (docs + market signals + tool registry)

## Running notebooks (per lecture)

Each lecture directory contains a `Makefile`, `Dockerfile`, and `pyproject.toml`.

From a lecture directory (e.g. `lecture_2/`):
- `make build`
- `make notebook` (starts Jupyter in Docker on port 8888)
- `make interactive` (drops you into a bash shell in the container)

## Building slides

Slides are in Beamer (LaTeX) under each lecture’s `slides/` folder.

Example:
```bash
cd lecture_1/slides
pdflatex lecture_1.tex
```
