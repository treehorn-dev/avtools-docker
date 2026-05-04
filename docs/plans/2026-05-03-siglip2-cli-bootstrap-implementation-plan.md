# SigLIP2 CLI Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a generic SigLIP2 embedding CLI to the CPU utils image without turning `avtools-docker` into a project-specific application repo.

**Architecture:** Keep the utility repo narrow. Add one standalone Python CLI script that can embed one or more image files and write `.npy` plus optional JSON metadata. Bake only the tool runtime into the CPU image: the script, its generic ML dependencies, and a smoke path that proves the command is present. Do not add video-specific logic or project-specific schemas yet.

**Tech Stack:** Docker, Ubuntu 24.04 LTS, Python 3, transformers, torch, numpy, Pillow, pytest, Make

### Task 1: Extend the scaffold contract tests

**Files:**
- Modify: `tests/test_repo_layout.py`
- Test: `tests/test_repo_layout.py`

**Step 1: Write the failing test**
Add assertions that require:
- `scripts/siglip2_embed.py` to exist
- `Dockerfile.utils-cpu` to mention `transformers` and `siglip2_embed.py`
- `scripts/smoke-cpu.sh` to check `siglip2-embed`

**Step 2: Run test to verify it fails**
Run: `. .venv/bin/activate && pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`
Expected: FAIL because the script and Dockerfile wiring do not exist yet.

**Step 3: Write minimal implementation**
Only after seeing the failures, add the minimum repo files and wiring needed to satisfy the new contract.

**Step 4: Run test to verify it passes**
Run: `. .venv/bin/activate && pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`
Expected: PASS.

### Task 2: Add the standalone SigLIP2 CLI

**Files:**
- Create: `scripts/siglip2_embed.py`
- Modify: `Dockerfile.utils-cpu`
- Modify: `scripts/smoke-cpu.sh`
- Modify: `README.md`

**Step 1: Write the failing test**
Use the contract test from Task 1; do not add image-model behavior tests yet.

**Step 2: Run test to verify it fails**
Run the same `pytest` command as Task 1.
Expected: FAIL.

**Step 3: Write minimal implementation**
Implement a CLI that:
- accepts one or more `--image` paths
- accepts `--output-npy` and optional `--output-json`
- defers heavy imports until execution so `--help` remains lightweight
- uses `google/siglip2-base-patch16-256` by default
- writes stacked embeddings via `numpy.save`

In the Dockerfile:
- install `numpy`, `pillow`, `transformers`
- copy the script into `/usr/local/bin/siglip2-embed`
- mark it executable

In the smoke script:
- assert `siglip2-embed` exists
- run `siglip2-embed --help`

**Step 4: Run test to verify it passes**
Run: `. .venv/bin/activate && pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`
Expected: PASS.

### Task 3: Verify repo-local and container-facing paths

**Files:**
- Modify: `Makefile`
- Modify: `pyproject.toml`
- Modify: `README.md`

**Step 1: Write the failing test**
Extend the repo contract test only if needed to require `make test` and the documented smoke/build flow.

**Step 2: Run test to verify it fails**
Run the same `pytest` command.
Expected: FAIL if the repo contract changed.

**Step 3: Write minimal implementation**
Keep `make test`, `make build-cpu`, and `make smoke-cpu` as the only supported local flow. Document the SigLIP2 utility briefly in `README.md`.

**Step 4: Run test to verify it passes**
Run: `. .venv/bin/activate && pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`
Expected: PASS.

### Task 4: Verify the result

**Files:**
- No code changes required unless verification fails

**Step 1: Run repo-local tests**
Run: `make test`
Expected: PASS.

**Step 2: Verify the image build path**
Run: `make build-cpu`
Expected: CPU image builds, acknowledging that heavyweight ML dependencies may take time.

**Step 3: Verify the smoke path**
Run: `make smoke-cpu`
Expected: container reports `ffmpeg`, `ffprobe`, `python`, `allin1`, and `siglip2-embed` as available.
