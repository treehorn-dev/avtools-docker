# avtools-docker

CPU/GPU media-utils image family for ffmpeg, ffmpeg-onnx-style tooling, allin1, SigLIP2 embedding, and avtools-adjacent workflows.

## Current Scope

This repo is intentionally narrow:
- CPU-first image family
- media/tooling substrate only
- no project app code baked into the image
- local pytest harness for scaffold verification
- generic `siglip2-embed` utility for per-image embedding generation
- filtered support-stack requirements plus ordered `allin1` bootstrap

## Components

## Final Image

`make build-cpu` builds the lean default CPU image. `make build-cpu-warm` builds the heavier warmed variant. The CPU image contains:
- `allin1`
- `siglip2-embed`
- `transnetv2-cli`
- `ffmpeg-onnx` plus the baked runtime and NudeNet assets
- `wd14-tagger`
- `transnetv2-cli` plus bundled `transnetv2pt` weights

The warmed CPU image additionally contains:
- `wd14-tagger` default ConvNeXTV2 model baked from Hugging Face
- warmed `allin1` caches
- warmed SigLIP2 caches

The component-specific build targets remain available for isolated verification and debugging.

`allin1` is currently installed into the main utils CPU image.

`ffmpeg-onnx` is carried separately as a git submodule at `third_party/ffmpeg-onnx`. It stays its own component and image for now rather than being collapsed into `Dockerfile.utils-cpu`.

Build that component directly with:

```bash
make build-ffmpeg-onnx
```

For the release-backed baked model flow:

```bash
make fetch-ffmpeg-onnx-assets
make build-ffmpeg-onnx-base
make build-ffmpeg-onnx-baked
```

`wd14-tagger-standalone` is also carried separately as a git submodule at `third_party/wd14-tagger-standalone`. Build its standalone CPU image with:

```bash
make build-wd14-cpu
```

That component fetches the default ConvNeXTV2 model directly from Hugging Face during the image build.

`transnetv2-cli` is carried as a git submodule at `third_party/transnetv2-cli`. Build its standalone CPU image with:

```bash
make build-transnetv2-cpu
```

That component relies on packaged `transnetv2pt` weights, so it does not need a separate release asset flow.

## Local Verification

```bash
make test
```

## Build

```bash
make build-cpu
make build-cpu-warm
```

## CI Publish Tags

Woodpecker currently publishes only the CPU variants to GHCR:

- `ghcr.io/treehorn-dev/avtools-utils:cpu`
- `ghcr.io/treehorn-dev/avtools-utils:cpu-latest`
- `ghcr.io/treehorn-dev/avtools-utils:cpu-warm`
- `ghcr.io/treehorn-dev/avtools-utils:cpu-warm-latest`

There is intentionally no bare `latest` tag.

## Smoke Test

```bash
make smoke-cpu
make smoke-cpu-warm
```

The smoke target bind-mounts this repo at `/workspace` so the container can execute `scripts/smoke-cpu.sh` without baking repo files into the image.

## Why Python 3.10 Right Now

The combined image is currently anchored to the `ffmpeg-onnx:baked` base and the working `allin1` stack. In practice that means the shipped integrator image is on Python `3.10`, even though some component repos can target newer runtimes independently.

## Dependency Strategy

The CPU image now follows the only fork recipe that showed credible operational evidence:

1. install build tooling
2. bootstrap `torch`, `torchvision`, `torchaudio`, and `cython`
3. install a filtered support stack from `requirements/utils-cpu.txt`
4. install `madmom`
5. install `natten==0.15.0`
6. install `allin1` from the `docker-audio-tools/all-in-one-docker-cpu-apple-silicon` source tree
7. compose in `wd14-tagger-standalone` and `ffmpeg-onnx` after those stacks are stable

This is deliberate. `allin1` packaging is too fragile to treat as a normal one-line pip dependency.

## SigLIP2 CLI

The CPU image installs `siglip2-embed`, a generic per-image embedding utility.

```bash
siglip2-embed \
  --image /data/frame-001.jpg \
  --image /data/frame-002.jpg \
  --output-npy /data/embeddings.npy \
  --output-json /data/embeddings.json
```

By default it uses `google/siglip2-base-patch16-naflex` on `cpu`.

The warmed CPU image build runs a tiny warm-cache step during packaging:
- a synthetic `wav` through `allin1`
- a synthetic `jpg` through `siglip2-embed`

That forces the heavy first-run assets into the image instead of making the first real invocation pay the setup cost. The cool image skips that step.

## Planned Next Steps

- validate whether the combined image still stays healthy as we add more utilities
- decide whether to vendor the `natten_compat.py` patch instead of relying on the fork source tree
- add GPU variant
- extend CI from `cpu` / `cpu-warm` to the full `cpu/gpu` x `cool/warm` matrix
