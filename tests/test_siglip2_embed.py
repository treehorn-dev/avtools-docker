from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_siglip_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "siglip2_embed.py"
    spec = importlib.util.spec_from_file_location("siglip2_embed", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_args(
    *,
    images: list[str] | None = None,
    input_dirs: list[str] | None = None,
    recursive: bool = False,
) -> argparse.Namespace:
    return argparse.Namespace(
        images=images or [],
        input_dirs=input_dirs or [],
        recursive=recursive,
    )


def test_resolve_image_paths_accepts_repeated_images(tmp_path: Path) -> None:
    module = load_siglip_module()
    parser = module.build_parser()
    image_a = tmp_path / "b.jpg"
    image_b = tmp_path / "a.png"
    image_a.write_bytes(b"a")
    image_b.write_bytes(b"b")

    result = module.resolve_image_paths(
        make_args(images=[str(image_a), str(image_b)]),
        parser,
    )

    assert result == [image_a.resolve(), image_b.resolve()]


def test_resolve_image_paths_collects_top_level_directory_images_only(tmp_path: Path) -> None:
    module = load_siglip_module()
    parser = module.build_parser()
    root = tmp_path / "frames"
    nested = root / "nested"
    root.mkdir()
    nested.mkdir()
    keep_a = root / "b.jpg"
    keep_b = root / "a.png"
    ignore_nested = nested / "c.jpg"
    ignore_text = root / "note.txt"
    keep_a.write_bytes(b"a")
    keep_b.write_bytes(b"b")
    ignore_nested.write_bytes(b"c")
    ignore_text.write_text("x")

    result = module.resolve_image_paths(
        make_args(input_dirs=[str(root)]),
        parser,
    )

    assert result == [keep_b.resolve(), keep_a.resolve()]


def test_resolve_image_paths_collects_recursive_directory_images(tmp_path: Path) -> None:
    module = load_siglip_module()
    parser = module.build_parser()
    root = tmp_path / "frames"
    nested = root / "nested"
    deeper = nested / "deeper"
    root.mkdir()
    nested.mkdir()
    deeper.mkdir()
    top = root / "top.jpg"
    mid = nested / "mid.png"
    low = deeper / "low.webp"
    top.write_bytes(b"a")
    mid.write_bytes(b"b")
    low.write_bytes(b"c")

    result = module.resolve_image_paths(
        make_args(input_dirs=[str(root)], recursive=True),
        parser,
    )

    assert result == [low.resolve(), mid.resolve(), top.resolve()]


def test_resolve_image_paths_merges_explicit_images_and_directory_images(tmp_path: Path) -> None:
    module = load_siglip_module()
    parser = module.build_parser()
    explicit = tmp_path / "explicit.jpg"
    directory = tmp_path / "frames"
    discovered = directory / "frame-001.jpg"
    explicit.write_bytes(b"a")
    directory.mkdir()
    discovered.write_bytes(b"b")

    result = module.resolve_image_paths(
        make_args(images=[str(explicit)], input_dirs=[str(directory)]),
        parser,
    )

    assert result == [explicit.resolve(), discovered.resolve()]


def test_resolve_image_paths_requires_at_least_one_input_source(tmp_path: Path) -> None:
    module = load_siglip_module()
    parser = module.build_parser()

    try:
        module.resolve_image_paths(make_args(), parser)
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected parser error")
