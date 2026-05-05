from __future__ import annotations

from pathlib import Path


def test_repo_has_initial_cpu_layout() -> None:
    assert Path('Dockerfile.assets').exists()
    assert Path('Dockerfile.utils-cpu').exists()
    assert Path('Dockerfile.utils-cpu-warm').exists()
    assert Path('Dockerfile.utils-gpu').exists()
    assert Path('Dockerfile.utils-gpu-warm').exists()
    assert Path('Makefile').exists()
    assert Path('README.md').exists()
    assert Path('.woodpecker.yml').exists()
    assert Path('.gitmodules').exists()
    assert Path('pyproject.toml').exists()
    assert Path('requirements/utils-cpu.txt').exists()
    assert Path('requirements/utils-gpu-constraints.txt').exists()
    assert Path('scripts/smoke-cpu.sh').exists()
    assert Path('scripts/siglip2_embed.py').exists()
    assert Path('scripts/warm-models.sh').exists()
    assert Path('third_party/ffmpeg-onnx').exists()
    assert Path('third_party/wd14-tagger-standalone').exists()
    assert Path('third_party/transnetv2-cli').exists()


def test_cpu_dockerfile_uses_ffmpeg_onnx_base_and_composes_component_tools() -> None:
    text = Path('Dockerfile.utils-cpu').read_text()

    assert 'ARG FFMPEG_ONNX_BASE_IMAGE=ffmpeg-onnx:baked' in text
    assert 'FROM ${FFMPEG_ONNX_BASE_IMAGE}' in text
    assert 'ARG OCI_REVISION=unknown' in text
    assert 'ARG OCI_SOURCE=https://github.com/treehorn-dev/avtools-docker' in text
    assert 'ARG OCI_CREATED=unknown' in text
    assert 'org.opencontainers.image.revision="${OCI_REVISION}"' in text
    assert 'python3.10-dev' in text
    assert 'python-is-python3' in text
    assert 'python3.10-venv' in text
    assert 'COPY requirements/utils-cpu.txt' in text
    assert 'COPY third_party/wd14-tagger-standalone /tmp/wd14-tagger-standalone' in text
    assert 'COPY third_party/transnetv2-cli /tmp/transnetv2-cli' in text
    assert 'ARG MADMOM_REPO=https://github.com/CPJKU/madmom' in text
    assert 'ARG MADMOM_REF=27f032e8947204902c675e5e341a3faf5dc86dae' in text
    assert 'ARG BAKE_WD14_ASSETS=0' in text
    assert 'ARG WARM_MODELS=0' in text
    assert 'pip3 install --upgrade pip setuptools wheel' in text
    assert 'pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2' in text
    assert 'pip3 install --no-cache-dir cython' in text
    assert 'pip3 install --no-cache-dir -r /tmp/utils-cpu.txt' in text
    assert 'pip3 install --no-cache-dir git+${MADMOM_REPO}@${MADMOM_REF}' in text
    assert 'pip3 install --no-cache-dir --no-build-isolation natten==0.15.0' in text
    assert 'git clone --depth=1 --branch "${ALLIN1_REF}" "${ALLIN1_REPO}" /tmp/all-in-one' in text
    assert 'pip3 install --no-cache-dir /tmp/all-in-one' in text
    assert "sed -i 's/requires-python = \">=3.11\"/requires-python = \">=3.10\"/' /tmp/wd14-tagger-standalone/pyproject.toml" in text
    assert '/opt/wd14-venv/bin/pip install --no-cache-dir /tmp/wd14-tagger-standalone' in text
    assert 'ln -s /opt/wd14-venv/bin/wd14-tagger /usr/local/bin/wd14-tagger' in text
    assert 'rm -rf /tmp/wd14-tagger-standalone' in text
    assert 'COPY third_party/wd14-tagger-standalone/scripts/fetch-hf-assets.sh /usr/local/bin/fetch-wd14-assets' in text
    assert 'RUN if [ "$BAKE_WD14_ASSETS" = "1" ]; then /bin/sh /usr/local/bin/fetch-wd14-assets /opt/wd14-models/wd14-convnextv2.v1; fi' in text
    assert 'pip3 install --no-cache-dir opencv-python-headless==4.10.0.84' in text
    assert "sed -i 's/requires-python = \"'>=3.11\"/requires-python = \"'>=3.10\"/' /tmp/transnetv2-cli/pyproject.toml" not in text
    assert "sed -i 's/requires-python = \"'>=3.11\"/requires-python = \"'>=3.10\"/' /tmp/transnetv2-cli/pyproject.toml" not in text
    assert "sed -i 's/requires-python = \">=3.11\"/requires-python = \">=3.10\"/' /tmp/transnetv2-cli/pyproject.toml" in text
    assert 'python3 -m venv /opt/transnetv2-venv --system-site-packages' in text
    assert '/opt/transnetv2-venv/bin/pip install --no-cache-dir future ffmpeg-python' in text
    assert '/opt/transnetv2-venv/bin/pip install --no-cache-dir --no-deps git+https://github.com/badde57/transnetv2pt.git@v1.0.0' in text
    assert '/opt/transnetv2-venv/bin/pip install --no-cache-dir --no-deps /tmp/transnetv2-cli' in text
    assert 'ln -s /opt/transnetv2-venv/bin/transnetv2-cli /usr/local/bin/transnetv2-cli' in text
    assert 'COPY scripts/warm-models.sh /usr/local/bin/warm-models' in text
    assert 'RUN chmod +x /usr/local/bin/siglip2-embed /usr/local/bin/warm-models /usr/local/bin/fetch-wd14-assets' in text
    assert 'RUN if [ "$WARM_MODELS" = "1" ]; then /usr/local/bin/warm-models; fi' in text
    assert 'ENTRYPOINT ["bash"]' in text
    assert 'siglip2-embed' in text


def test_makefile_exposes_build_test_and_smoke_targets() -> None:
    text = Path('Makefile').read_text()

    assert 'build-cpu:' in text
    assert 'build-assets-cpu:' in text
    assert 'build-cpu-warm:' in text
    assert 'build-gpu:' in text
    assert 'build-assets-gpu:' in text
    assert 'build-gpu-warm:' in text
    assert 'build-ffmpeg-onnx:' in text
    assert 'build-ffmpeg-onnx-base:' in text
    assert 'fetch-ffmpeg-onnx-assets:' in text
    assert 'build-ffmpeg-onnx-baked:' in text
    assert 'build-wd14-cpu:' in text
    assert 'build-transnetv2-cpu:' in text
    assert 'test:' in text
    assert 'smoke-cpu:' in text
    assert 'smoke-cpu-warm:' in text
    assert 'docker build -f Dockerfile.utils-cpu --build-arg BAKE_WD14_ASSETS=0 --build-arg WARM_MODELS=0 -t $(IMAGE_CPU) .' in text
    assert 'docker build -f Dockerfile.assets --build-arg BAKE_WD14_ASSETS=1 --build-arg FETCH_SIGLIP_ASSETS=1 --build-arg FETCH_ALLIN1_ASSETS=1 -t $(IMAGE_ASSETS_CPU) .' in text
    assert 'docker build -f Dockerfile.utils-cpu-warm --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_CPU) --build-arg AVTOOLS_ASSETS_IMAGE=$(IMAGE_ASSETS_CPU) -t $(IMAGE_CPU_WARM) .' in text
    assert 'docker build -f Dockerfile.utils-gpu --build-arg BAKE_WD14_ASSETS=0 --build-arg WARM_MODELS=0 -t $(IMAGE_GPU) .' in text
    assert 'docker build -f Dockerfile.assets --build-arg BAKE_WD14_ASSETS=1 --build-arg FETCH_SIGLIP_ASSETS=1 --build-arg FETCH_ALLIN1_ASSETS=1 -t $(IMAGE_ASSETS_GPU) .' in text
    assert 'docker build -f Dockerfile.utils-gpu-warm --build-arg AVTOOLS_BASE_IMAGE=$(IMAGE_GPU) --build-arg AVTOOLS_ASSETS_IMAGE=$(IMAGE_ASSETS_GPU) -t $(IMAGE_GPU_WARM) .' in text
    assert 'docker build -t ffmpeg-onnx:cpu third_party/ffmpeg-onnx' in text
    assert 'docker build -t ffmpeg-onnx-base third_party/ffmpeg-onnx' in text
    assert 'bash ./scripts/fetch-release-assets.sh nudenet-assets-v1' in text
    assert 'docker build -t ffmpeg-onnx:baked -f third_party/ffmpeg-onnx/Dockerfile.baked third_party/ffmpeg-onnx' in text
    assert 'docker build -t wd14-tagger:cpu -f third_party/wd14-tagger-standalone/Dockerfile.cpu third_party/wd14-tagger-standalone' in text
    assert 'docker build -t $(TRANSNETV2_IMAGE) -f third_party/transnetv2-cli/Dockerfile.cpu third_party/transnetv2-cli' in text
    assert '.venv/bin/python -m pytest -q' in text


def test_pyproject_declares_pytest_dev_harness() -> None:
    text = Path('pyproject.toml').read_text()

    assert '[project]' in text
    assert 'pytest' in text
    assert '[tool.pytest.ini_options]' in text


def test_readme_mentions_component_boundaries_and_final_image() -> None:
    text = Path('README.md').read_text()

    assert 'third_party/ffmpeg-onnx' in text
    assert 'third_party/wd14-tagger-standalone' in text
    assert 'third_party/transnetv2-cli' in text
    assert 'make build-ffmpeg-onnx' in text
    assert 'make fetch-ffmpeg-onnx-assets' in text
    assert 'make build-ffmpeg-onnx-base' in text
    assert 'make build-ffmpeg-onnx-baked' in text
    assert 'make build-wd14-cpu' in text
    assert 'make build-transnetv2-cpu' in text
    assert 'make build-cpu' in text
    assert 'make build-assets-cpu' in text
    assert 'make build-cpu-warm' in text
    assert 'make build-gpu' in text
    assert 'make build-assets-gpu' in text
    assert 'make build-gpu-warm' in text
    assert 'The dedicated assets image family currently bakes' in text
    assert 'without waiting for the full runtime image' in text


def test_assets_and_warm_dockerfiles_use_copy_layers() -> None:
    assets_text = Path('Dockerfile.assets').read_text()
    cpu_text = Path('Dockerfile.utils-cpu-warm').read_text()
    gpu_text = Path('Dockerfile.utils-gpu-warm').read_text()

    assert 'ARG PYTHON_BASE_IMAGE=ghcr.io/treehorn-dev/ffmpeg-onnx:baked-latest' in assets_text
    assert 'FROM ${PYTHON_BASE_IMAGE}' in assets_text
    assert 'ARG FETCH_ALLIN1_ASSETS=1' in assets_text
    assert 'ARG FETCH_SIGLIP_ASSETS=1' in assets_text
    assert 'ARG ALLIN1_DEMUCS_URL=https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th' in assets_text
    assert 'ENV HF_HOME=/opt/hf-cache' in assets_text
    assert 'ENV TORCH_HOME=/opt/torch-cache' in assets_text
    assert '/usr/local/bin/fetch-wd14-assets' in assets_text
    assert 'python3 -c' in assets_text
    assert 'snapshot_download(' in assets_text
    assert '955717e8-8726e21a.th' in assets_text
    assert 'ARG AVTOOLS_BASE_IMAGE=avtools-utils:cpu' in cpu_text
    assert 'ARG AVTOOLS_ASSETS_IMAGE=avtools-assets:cpu' in cpu_text
    assert 'FROM ${AVTOOLS_ASSETS_IMAGE} AS assets' in cpu_text
    assert 'FROM ${AVTOOLS_BASE_IMAGE}' in cpu_text
    assert 'COPY --from=assets /opt/hf-cache /opt/hf-cache' in cpu_text
    assert 'COPY --from=assets /opt/torch-cache /opt/torch-cache' in cpu_text
    assert 'COPY --from=assets /opt/wd14-models /opt/wd14-models' in cpu_text
    assert 'ARG AVTOOLS_BASE_IMAGE=avtools-utils:gpu' in gpu_text
    assert 'ARG AVTOOLS_ASSETS_IMAGE=avtools-assets:gpu' in gpu_text
    assert 'FROM ${AVTOOLS_ASSETS_IMAGE} AS assets' in gpu_text
    assert 'FROM ${AVTOOLS_BASE_IMAGE}' in gpu_text
    assert 'COPY --from=assets /opt/hf-cache /opt/hf-cache' in gpu_text
    assert 'COPY --from=assets /opt/torch-cache /opt/torch-cache' in gpu_text
    assert 'COPY --from=assets /opt/wd14-models /opt/wd14-models' in gpu_text


def test_gpu_dockerfile_redeclares_jellyfin_version_after_from() -> None:
    text = Path('Dockerfile.utils-gpu').read_text()
    constraints = Path('requirements/utils-gpu-constraints.txt').read_text()

    assert 'ARG JELLYFIN_FFMPEG_VERSION=7.1.3-6\nFROM ${CUDA_BASE_IMAGE}' in text
    assert 'FROM ${CUDA_BASE_IMAGE}\n\nARG DEBIAN_FRONTEND=noninteractive\nARG TARGETARCH=amd64\nARG JELLYFIN_FFMPEG_VERSION=7.1.3-6' in text
    assert 'ARG OCI_REVISION=unknown' in text
    assert 'ARG OCI_SOURCE=https://github.com/treehorn-dev/avtools-docker' in text
    assert 'org.opencontainers.image.revision="${OCI_REVISION}"' in text
    assert '--index-url https://download.pytorch.org/whl/cu124' in text
    assert 'torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0' in text
    assert 'torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 cython' not in text
    assert 'RUN pip3 install --no-cache-dir cython' in text
    assert 'COPY requirements/utils-gpu-constraints.txt /tmp/utils-gpu-constraints.txt' in text
    assert "RUN sed -i 's/^sympy==1.13.3$/sympy==1.13.1/' /tmp/utils-cpu.txt" in text
    assert 'RUN pip3 install --no-cache-dir -c /tmp/utils-gpu-constraints.txt -r /tmp/utils-cpu.txt' in text
    assert 'sympy==1.13.1' in constraints
    assert 'natten==0.17.5+torch250cu124 -f https://whl.natten.org' in text
    assert 'python3 -c "import torch; assert torch.__version__ == \\"2.5.0+cu124\\"' in text


def test_smoke_script_checks_composed_tooling() -> None:
    text = Path('scripts/smoke-cpu.sh').read_text()

    assert 'siglip2-embed' in text
    assert 'ffmpeg-onnx' in text
    assert 'wd14-tagger' in text
    assert 'transnetv2-cli' in text
    assert '--help' in text


def test_cpu_requirements_pin_filtered_support_stack() -> None:
    text = Path('requirements/utils-cpu.txt').read_text()

    assert 'demucs==4.0.1' in text
    assert 'librosa==0.11.0' in text
    assert 'onnxruntime==1.20.1' in text
    assert 'sentencepiece' in text
    assert 'transformers' in text
    assert 'google/siglip2-base-patch16-naflex' in Path('scripts/siglip2_embed.py').read_text()
    assert 'allin1' not in text
    assert 'natten' not in text
    assert 'torchvision' not in text


def test_warm_script_warms_allin1_and_siglip() -> None:
    text = Path('scripts/warm-models.sh').read_text()

    assert 'export HF_HUB_DISABLE_XET=1' in text
    assert 'python3 -m allin1.cli' in text
    assert 'if [ "${WARM_ALLIN1:-1}" = "1" ]; then' in text
    assert 'siglip2-embed' in text
    assert 'google/siglip2-base-patch16-naflex' in text
    assert 'warm.wav' in text
    assert 'rm -rf "${HF_HOME:-/opt/hf-cache}/xet"' in text


def test_siglip_embed_uses_slow_processor_path() -> None:
    text = Path('scripts/siglip2_embed.py').read_text()

    assert "AutoProcessor.from_pretrained(model_name, use_fast=False)" in text


def test_woodpecker_builds_and_publishes_runtime_and_asset_variants() -> None:
    text = Path('.woodpecker.yml').read_text()

    assert 'woodpeckerci/plugin-git' in text
    assert 'recursive: false' in text
    assert 'sync-submodules:' in text
    assert 'git submodule sync' in text
    assert 'git submodule update --init --recursive' in text
    assert 'publish-ffmpeg-onnx-base:' in text
    assert 'publish-ffmpeg-onnx-baked:' in text
    assert 'woodpeckerci/plugin-kaniko' in text
    assert 'ghcr.io/treehorn-dev/ffmpeg-onnx' in text
    assert 'third_party/ffmpeg-onnx/Dockerfile.baked' in text
    assert 'build_args:' in text
    assert '- FFMPEG_ONNX_BASE_IMAGE=ghcr.io/treehorn-dev/ffmpeg-onnx:base-${CI_COMMIT_SHA:0:7}' in text
    assert '- FFMPEG_ONNX_BASE_IMAGE=ghcr.io/treehorn-dev/ffmpeg-onnx:baked-${CI_COMMIT_SHA:0:7}' in text
    assert 'publish-cpu:' in text
    assert 'publish-assets-cpu:' in text
    assert 'publish-cpu-warm:' in text
    assert 'depends_on:\n      - publish-ffmpeg-onnx-baked' in text
    assert 'depends_on:\n      - publish-assets-cpu\n      - publish-cpu' in text
    assert 'dockerfile: Dockerfile.utils-cpu-warm' in text
    assert 'publish-gpu:' in text
    assert 'publish-assets-gpu:' in text
    assert 'publish-gpu-warm:' in text
    assert 'depends_on:\n      - publish-assets-gpu\n      - publish-gpu' in text
    assert 'dockerfile: Dockerfile.assets' in text
    assert 'dockerfile: Dockerfile.utils-gpu' in text
    assert 'dockerfile: Dockerfile.utils-gpu-warm' in text
    assert 'ghcr.io/treehorn-dev/avtools-utils' in text
    assert 'ghcr.io/treehorn-dev/avtools-assets' in text
    assert '- BAKE_WD14_ASSETS=0' in text
    assert '- WARM_MODELS=0' in text
    assert '- BAKE_WD14_ASSETS=1' in text
    assert '- FETCH_SIGLIP_ASSETS=1' in text
    assert '- FETCH_ALLIN1_ASSETS=1' in text
    assert '- PYTHON_BASE_IMAGE=ghcr.io/treehorn-dev/ffmpeg-onnx:baked-${CI_COMMIT_SHA:0:7}' in text
    assert '- AVTOOLS_ASSETS_IMAGE=ghcr.io/treehorn-dev/avtools-assets:cpu-${CI_COMMIT_SHA:0:7}' in text
    assert '- AVTOOLS_ASSETS_IMAGE=ghcr.io/treehorn-dev/avtools-assets:gpu-${CI_COMMIT_SHA:0:7}' in text
    assert 'treehorn-dev_ghcr_username' in text
    assert 'treehorn-dev_ghcr_token' in text
    assert 'build-args-from-env' not in text
    assert '\n    environment:\n' not in text
    assert '- cpu' in text
    assert '- cpu-latest' in text
    assert '- cpu-${CI_COMMIT_SHA:0:7}' in text
    assert '- cpu-warm' in text
    assert '- cpu-warm-latest' in text
    assert '- cpu-warm-${CI_COMMIT_SHA:0:7}' in text
    assert '- gpu' in text
    assert '- gpu-latest' in text
    assert '- gpu-${CI_COMMIT_SHA:0:7}' in text
    assert 'Dockerfile.utils-cpu' in text
    assert 'Dockerfile.utils-cpu-warm' in text
    assert '- gpu-warm' in text
    assert '- gpu-warm-latest' in text
    assert '- gpu-warm-${CI_COMMIT_SHA:0:7}' in text
    assert '- base-${CI_COMMIT_SHA:0:7}' in text
    assert '- baked-${CI_COMMIT_SHA:0:7}' in text
    assert '- cpu-warm-${CI_COMMIT_SHA:0:7}' in text
    assert '- gpu-warm-${CI_COMMIT_SHA:0:7}' in text
    assert '- OCI_REVISION=${CI_COMMIT_SHA:0:7}' in text
    assert '- OCI_CREATED=${CI_PIPELINE_CREATED}' in text
