#!/usr/bin/env python3
"""Deliver the 26 November 2026 front page for make.fun news-image-20261126.

The entry image is a pre-rendered PNG vendored beside this script
(entry.png, 1024x1024, 8-bit palette). The program performs no drawing
and no network access: it reads the vendored artwork, checks it is a
complete, well-formed PNG of the expected size and digest, and copies
those exact bytes to the output directory the harness provides.

Run:  MAKEFUN_OUTPUT_DIR=<dir> python3 main.py
"""

import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTWORK = HERE / "entry.png"

# Digest of the vendored front page for 26 November 2026.
EXPECTED_SHA256 = "e8f31923ef4793c6d843365a4e33e35cbde08dd7ea2b35f87f97ad0b40d9c9e7"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # entry image must fit in 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Abort with a clear error on stderr and a non-zero exit."""
    print(f"main.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_artwork():
    """Read the vendored PNG bytes, refusing files too short to hold one."""
    try:
        blob = ARTWORK.read_bytes()
    except OSError as exc:
        fail(f"cannot read {ARTWORK.name}: {exc}")
    if len(blob) > MAX_BYTES:
        fail(f"{ARTWORK.name} is {len(blob)} bytes, over the 1 MiB cap")
    if len(blob) < 8:
        fail(f"{ARTWORK.name} is too short to be a PNG")
    return blob


def check_png(blob):
    """Validate the PNG structure end to end: signature, header, chunks."""
    if blob[:8] != PNG_MAGIC:
        fail("not a PNG file: bad 8-byte signature")
    first_len = struct.unpack(">I", blob[8:12])[0]
    first_type = blob[12:16]
    if first_type != b"IHDR" or first_len != 13:
        fail(f"first chunk is {first_type!r} ({first_len} bytes), "
             "expected a 13-byte IHDR")
    width, height, depth, colour = struct.unpack(">IIBB", blob[16:26])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(f"page is {width}x{height}, expected "
             f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    if depth != 8:
        fail(f"bit depth is {depth}, expected 8")
    if colour not in (2, 3):
        fail(f"colour type is {colour}, expected 2 (RGB) or 3 (palette)")
    pos = 8
    seen_iend = False
    while pos + 8 <= len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        ctype = blob[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(blob):
            fail(f"chunk {ctype!r} overruns the file")
        stored_crc = struct.unpack(">I", blob[pos + 8 + length:end])[0]
        actual_crc = zlib.crc32(blob[pos + 4:pos + 8 + length]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"chunk {ctype!r} has a bad CRC")
        pos = end
        if ctype == b"IEND":
            seen_iend = True
            break
    if not seen_iend:
        fail("no IEND chunk: PNG is truncated")
    if pos != len(blob):
        fail("trailing bytes after the IEND chunk")


def check_digest(blob):
    """Confirm the artwork is exactly the front page this program ships."""
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        fail(f"sha256 mismatch: got {digest}, "
             f"expected {EXPECTED_SHA256}")


def deliver(blob):
    """Write the validated bytes to $MAKEFUN_OUTPUT_DIR/entry.png."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes, "
          f"sha256 {hashlib.sha256(blob).hexdigest()[:16]}...)")


def main():
    blob = load_artwork()
    check_png(blob)
    check_digest(blob)
    deliver(blob)


if __name__ == "__main__":
    main()
