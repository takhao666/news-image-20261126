"""Entry for news-image-20261126: \"26 November 2026 — The World in One Image\".

The image is a newspaper front page summarising the world news of
Thursday 26 November 2026 (US tariffs on India, the first Pakistani
astronaut aboard China's Shenzhou-24, North Korea expelling the Swiss
envoy, Thanksgiving in the US, Bangladesh's garment pay rise, and
Colombia's ten years of peace). It is stored in this repository as
entry.png; this program simply publishes those exact bytes to the
output path the grader reads, with no network and no randomness.
"""

import hashlib
import os
import sys

# The image this entry ships, next to this file in the repository.
SOURCE_NAME = "entry.png"

# Competition limits for the artifact (see RULES.txt).
MAX_BYTES = 1_048_576
MAX_SIDE_PX = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _png_dimensions(data: bytes):
    """Width and height read from the PNG IHDR chunk (bytes 16..24)."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def _repo_dir() -> str:
    """Directory holding this program (the repository root)."""
    return os.path.dirname(os.path.abspath(__file__))


def _output_path() -> str:
    """Where the grader expects the image; honour MAKEFUN_OUTPUT_DIR."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def _read_source() -> bytes:
    path = os.path.join(_repo_dir(), SOURCE_NAME)
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    width, height = _png_dimensions(data)
    if width > MAX_SIDE_PX or height > MAX_SIDE_PX:
        raise SystemExit("entry.png is over the 1024px limit")
    return data


def main() -> int:
    data = _read_source()
    dest = _output_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as handle:
        handle.write(data)
    # Confirm the copy is byte-identical to the shipped image.
    with open(dest, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        raise SystemExit("output does not match the shipped image")
    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
