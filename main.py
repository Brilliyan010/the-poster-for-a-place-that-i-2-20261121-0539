#!/usr/bin/env python3
"""LUMARIS — The Poster for a Place That Isn't There.

The repository holds the finished travel poster (entry.png), drawn
programmatically with PIL by gen_poster.py in the build session: a
vintage flat-style poster for the invented place LUMARIS, "Where the
Sun Rises Twice" — twin suns over a calm lagoon, a striped lighthouse
on a rocky isle, one small sailboat, and the place name set in large
type at the top. This program only copies that image to the make.fun
output directory.

Standard library only; deterministic — the same bytes every run.
The image is a whole 1024x1024 PNG, 222,570 bytes (limit 1 MiB).
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_MAGIC:
        print("entry.png: bad PNG magic", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png: over 1 MiB", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        print(f"entry.png: {width}x{height} exceeds 1024x1024", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
