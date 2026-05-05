IMAGE_CPU ?= avtools-utils:cpu
IMAGE_CPU_WARM ?= avtools-utils:cpu-warm
IMAGE_GPU ?= avtools-utils:gpu
IMAGE_GPU_WARM ?= avtools-utils:gpu-warm
IMAGE_ASSETS_CPU ?= avtools-assets:cpu
IMAGE_ASSETS_GPU ?= avtools-assets:gpu
FFMPEG_ONNX_IMAGE ?= ffmpeg-onnx:cpu
FFMPEG_ONNX_BASE_IMAGE ?= ffmpeg-onnx-base
FFMPEG_ONNX_BAKED_IMAGE ?= ffmpeg-onnx:baked
FFMPEG_ONNX_ASSET_TAG ?= nudenet-assets-v1
TRANSNETV2_IMAGE ?= transnetv2-cli:cpu
VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip

.PHONY: venv test build-cpu build-cpu-warm build-gpu build-gpu-warm build-assets-cpu build-assets-gpu build-ffmpeg-onnx build-ffmpeg-onnx-base fetch-ffmpeg-onnx-assets build-ffmpeg-onnx-baked build-wd14-cpu build-transnetv2-cpu smoke-cpu smoke-cpu-warm

venv:
	python3 -m venv $(VENV)
	$(PIP) install -U pip pytest

test: venv
	.venv/bin/python -m pytest -q

build-cpu:
	docker build -f Dockerfile.utils-cpu --build-arg BAKE_WD14_ASSETS=0 --build-arg WARM_MODELS=0 -t $(IMAGE_CPU) .

build-assets-cpu:
	docker build -f Dockerfile.assets --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_CPU) --build-arg BAKE_WD14_ASSETS=1 --build-arg WARM_MODELS=1 --build-arg WARM_ALLIN1=1 -t $(IMAGE_ASSETS_CPU) .

build-cpu-warm:
	docker build -f Dockerfile.utils-cpu-warm --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_CPU) --build-arg AVTOOLS_ASSETS_IMAGE=$(IMAGE_ASSETS_CPU) -t $(IMAGE_CPU_WARM) .

build-gpu:
	docker build -f Dockerfile.utils-gpu --build-arg BAKE_WD14_ASSETS=0 --build-arg WARM_MODELS=0 -t $(IMAGE_GPU) .

build-assets-gpu:
	docker build -f Dockerfile.assets --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_GPU) --build-arg BAKE_WD14_ASSETS=1 --build-arg WARM_MODELS=1 --build-arg WARM_ALLIN1=0 -t $(IMAGE_ASSETS_GPU) .

build-gpu-warm:
	docker build -f Dockerfile.utils-gpu-warm --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_GPU) --build-arg AVTOOLS_ASSETS_IMAGE=$(IMAGE_ASSETS_GPU) -t $(IMAGE_GPU_WARM) .

build-ffmpeg-onnx:
	docker build -t ffmpeg-onnx:cpu third_party/ffmpeg-onnx

build-ffmpeg-onnx-base:
	docker build -t ffmpeg-onnx-base third_party/ffmpeg-onnx

fetch-ffmpeg-onnx-assets:
	cd third_party/ffmpeg-onnx && bash ./scripts/fetch-release-assets.sh nudenet-assets-v1

build-ffmpeg-onnx-baked:
	docker build -t ffmpeg-onnx:baked -f third_party/ffmpeg-onnx/Dockerfile.baked third_party/ffmpeg-onnx

build-wd14-cpu:
	docker build -t wd14-tagger:cpu -f third_party/wd14-tagger-standalone/Dockerfile.cpu third_party/wd14-tagger-standalone

build-transnetv2-cpu:
	docker build -t $(TRANSNETV2_IMAGE) -f third_party/transnetv2-cli/Dockerfile.cpu third_party/transnetv2-cli

smoke-cpu:
	docker run --rm -v "$$(pwd)":/workspace -w /workspace $(IMAGE_CPU) scripts/smoke-cpu.sh

smoke-cpu-warm:
	docker run --rm -v "$$(pwd)":/workspace -w /workspace $(IMAGE_CPU_WARM) scripts/smoke-cpu.sh
