#!/usr/bin/env bash
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mkdir -p "${HF_HOME:-/opt/hf-cache}" "${TORCH_HOME:-/opt/torch-cache}"
export HF_HUB_DISABLE_XET=1

ffmpeg -loglevel error -y \
  -f lavfi -i "sine=frequency=440:duration=5" \
  -c:a pcm_s16le \
  "$tmpdir/warm.wav"

if [ "${WARM_ALLIN1:-1}" = "1" ]; then
  python3 -m allin1.cli "$tmpdir/warm.wav" --out-dir "$tmpdir/allin1"
fi

ffmpeg -loglevel error -y \
  -f lavfi -i "color=c=gray:size=256x256:duration=1" \
  -frames:v 1 \
  "$tmpdir/warm.jpg"

siglip2-embed \
  --image "$tmpdir/warm.jpg" \
  --output-npy "$tmpdir/siglip.npy" \
  --output-json "$tmpdir/siglip.json" \
  --model google/siglip2-base-patch16-naflex \
  --device cpu

rm -rf "${HF_HOME:-/opt/hf-cache}/xet"
rm -rf "${HF_HOME:-/opt/hf-cache}/.locks"
rm -rf "${HF_HOME:-/opt/hf-cache}/hub/.locks"
