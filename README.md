# 2026-AI-Development
Winter 2026 AI Development Training Series

## Workshop Structure

This repository contains materials for a four-part workshop on AI and Career Development at the University of Chicago.

### Lectures

- **Lecture 1**: Traditional lecture format covering LLMs, Agents, and MCP
- **Lectures 2-4**: Interactive format with Jupyter notebooks and slides

Each lecture directory contains:
- `notebooks/`: Jupyter notebooks for interactive exercises
- `slides/`: Beamer presentation slides (LaTeX)
- `data/`: Data files used in the lecture
- `Makefile`: Commands to run interactive sessions and notebooks
- `pyproject.toml`: Python dependencies
- `Dockerfile`: Containerized environment setup

### Usage

To use a lecture's interactive environment:

1. Navigate to the lecture directory (e.g., `lecture_1/`)
2. Build the Docker image: `make build`
3. Start an interactive bash session: `make interactive`
4. Start a Jupyter notebook: `make notebook`

The notebook will be available at `http://localhost:8888`

### Building Slides

To compile the Beamer slides, you'll need a LaTeX distribution installed. Then:

```bash
cd lecture_X/slides/
pdflatex lecture_X.tex
```

### Requirements

- Docker
- Make
- LaTeX distribution (for building slides)
