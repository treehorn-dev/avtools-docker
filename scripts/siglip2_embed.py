#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

IMAGE_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='siglip2-embed',
        description='Generate SigLIP2 image embeddings for one or more image files or directories.',
    )
    parser.add_argument(
        '--image',
        dest='images',
        action='append',
        help='Path to an input image. Repeat for multiple images.',
    )
    parser.add_argument(
        '--input-dir',
        dest='input_dirs',
        action='append',
        help='Path to a directory of images. Repeat for multiple directories.',
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Recursively discover images under each --input-dir.',
    )
    parser.add_argument(
        '--output-npy',
        required=True,
        help='Path to the output .npy file for stacked embeddings.',
    )
    parser.add_argument(
        '--output-json',
        help='Optional path to JSON metadata about embedded images.',
    )
    parser.add_argument(
        '--model',
        default='google/siglip2-base-patch16-naflex',
        help='Hugging Face model id to use for embedding generation.',
    )
    parser.add_argument(
        '--device',
        default='cpu',
        help='Torch device to use, for example cpu, cuda, or mps.',
    )
    return parser


def discover_directory_images(directory: Path, recursive: bool) -> list[Path]:
    pattern = '**/*' if recursive else '*'
    candidates = []
    for path in directory.glob(pattern):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            candidates.append(path.resolve())
    return sorted(candidates)


def resolve_image_paths(args: argparse.Namespace, parser: argparse.ArgumentParser) -> list[Path]:
    explicit_paths = [Path(path).expanduser().resolve() for path in (args.images or [])]
    input_dirs = [Path(path).expanduser().resolve() for path in (args.input_dirs or [])]

    if not explicit_paths and not input_dirs:
        parser.error('at least one --image or --input-dir is required')

    for image_path in explicit_paths:
        if not image_path.exists():
            parser.error(f'image not found: {image_path}')
        if not image_path.is_file():
            parser.error(f'image path is not a file: {image_path}')

    discovered_paths: list[Path] = []
    for input_dir in input_dirs:
        if not input_dir.exists():
            parser.error(f'input directory not found: {input_dir}')
        if not input_dir.is_dir():
            parser.error(f'input path is not a directory: {input_dir}')
        discovered_paths.extend(discover_directory_images(input_dir, args.recursive))

    # Preserve explicit ordering first, then deterministic directory discovery.
    ordered_paths: list[Path] = []
    seen: set[Path] = set()
    for path in [*explicit_paths, *discovered_paths]:
        if path not in seen:
            ordered_paths.append(path)
            seen.add(path)

    if not ordered_paths:
        parser.error('no input images found')

    return ordered_paths


def embed_images(image_paths: Sequence[Path], model_name: str, device: str):
    import numpy as np
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    processor = AutoProcessor.from_pretrained(model_name, use_fast=False)
    model = AutoModel.from_pretrained(model_name)
    model.to(device)
    model.eval()

    vectors = []
    metadata = []
    with torch.inference_mode():
        for image_path in image_paths:
            with Image.open(image_path) as image:
                rgb_image = image.convert('RGB')
                inputs = processor(images=rgb_image, return_tensors='pt')
            inputs = {key: value.to(device) for key, value in inputs.items()}
            outputs = model.get_image_features(**inputs)
            embedding = outputs[0].detach().cpu().numpy()
            vectors.append(embedding)
            metadata.append(
                {
                    'image_path': str(image_path),
                    'embedding_dim': int(embedding.shape[0]),
                    'model': model_name,
                    'device': device,
                }
            )

    return np.stack(vectors), metadata


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    image_paths = resolve_image_paths(args, parser)

    output_npy = Path(args.output_npy).expanduser().resolve()
    output_npy.parent.mkdir(parents=True, exist_ok=True)

    embeddings, metadata = embed_images(image_paths, args.model, args.device)

    import numpy as np

    np.save(output_npy, embeddings)

    if args.output_json:
        output_json = Path(args.output_json).expanduser().resolve()
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(metadata, indent=2) + '\n')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
