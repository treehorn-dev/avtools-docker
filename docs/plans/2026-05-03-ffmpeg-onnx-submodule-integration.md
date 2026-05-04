# ffmpeg-onnx Submodule Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `ffmpeg-onnx` to `avtools-docker` as a first-class component via git submodule and minimal build/docs/test integration.

**Architecture:** Keep `ffmpeg-onnx` as an independent repo and consume it from `avtools-docker` through `third_party/ffmpeg-onnx`. The utils repo should expose orchestration targets and documentation, but not yet collapse the component into the main CPU image.

**Tech Stack:** git submodules, Make, pytest, Docker

### Task 1: Add failing repo-layout expectations

**Files:**
- Modify: `tests/test_repo_layout.py`

**Step 1: Write the failing test**

Add assertions for:
- `.gitmodules` existing
- `third_party/ffmpeg-onnx` existing
- `Makefile` exposing `build-ffmpeg-onnx`
- `README.md` mentioning `third_party/ffmpeg-onnx`

**Step 2: Run test to verify it fails**

Run: `pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`

**Step 3: Implement minimal code**

Add the missing repo files/configuration so those assertions become true.

**Step 4: Run test to verify it passes**

Run: `pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`

### Task 2: Add the submodule and build target

**Files:**
- Create: `.gitmodules`
- Modify: `Makefile`

**Step 1: Add submodule**

Run:
`git submodule add https://github.com/treehorn-dev/ffmpeg-onnx.git third_party/ffmpeg-onnx`

**Step 2: Add Make target**

Add a `build-ffmpeg-onnx` target that runs:
`docker build -t ffmpeg-onnx:cpu third_party/ffmpeg-onnx`

**Step 3: Verify target textually**

Covered by repo-layout test.

### Task 3: Document the component boundary

**Files:**
- Modify: `README.md`

**Step 1: Add a short component section**

Document:
- `allin1` stays in the main utils image
- `ffmpeg-onnx` is carried as a submodule
- it is built separately for now

**Step 2: Add the build command**

Document:
`make build-ffmpeg-onnx`

### Task 4: Full verification

**Files:**
- Verify only

**Step 1: Run focused tests**

Run: `pytest -q tests/test_repo_layout.py -o cache_dir=/tmp/avtools-docker-pytest-cache`

**Step 2: Run full local harness**

Run: `make test`

**Step 3: Inspect git status**

Run: `git status --short`
