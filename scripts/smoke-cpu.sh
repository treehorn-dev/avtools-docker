#!/usr/bin/env bash
set -euo pipefail

command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
command -v python3 >/dev/null
command -v allin1 >/dev/null
command -v siglip2-embed >/dev/null
command -v ffmpeg-onnx >/dev/null
command -v wd14-tagger >/dev/null
command -v transnetv2-cli >/dev/null

echo "ffmpeg: $(ffmpeg -version | head -n 1)"
echo "ffprobe: $(ffprobe -version | head -n 1)"
echo "python: $(python3 --version)"
echo "allin1: $(allin1 --help >/dev/null 2>&1 && echo ok)"
echo "siglip2-embed: $(siglip2-embed --help >/dev/null 2>&1 && echo ok)"
echo "ffmpeg-onnx: $(ffmpeg-onnx >/dev/null 2>&1 && echo ok)"
echo "wd14-tagger: $(wd14-tagger >/dev/null 2>&1 && echo ok)"
echo "transnetv2-cli: $(transnetv2-cli >/dev/null 2>&1 && echo ok)"
