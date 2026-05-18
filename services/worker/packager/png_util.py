"""Minimal PNG encoder (RGBA) without Pillow."""
from __future__ import annotations

import struct
import zlib


def encode_png_rgba(width: int, height: int, pixels: bytes) -> bytes:
    if len(pixels) != width * height * 4:
        raise ValueError("pixel buffer size mismatch")
    raw = b"".join(
        b"\x00" + pixels[y * width * 4 : (y + 1) * width * 4] for y in range(height)
    )
    compressed = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def solid_png(width: int, height: int, rgba: tuple[int, int, int, int]) -> bytes:
    r, g, b, a = rgba
    row = bytes([r, g, b, a] * width)
    pixels = row * height
    return encode_png_rgba(width, height, pixels)


def resize_cover_rgba(
    src_w: int,
    src_h: int,
    src: bytes,
    out_w: int,
    out_h: int,
) -> bytes:
    """Nearest-neighbor cover crop to out_w x out_h."""
    scale = max(out_w / src_w, out_h / src_h)
    nw = max(1, int(src_w * scale))
    nh = max(1, int(src_h * scale))
    ox = (nw - out_w) // 2
    oy = (nh - out_h) // 2
    out = bytearray(out_w * out_h * 4)
    for y in range(out_h):
        sy = min(nh - 1, int((y + oy) / scale))
        for x in range(out_w):
            sx = min(nw - 1, int((x + ox) / scale))
            si = (sy * src_w + sx) * 4
            oi = (y * out_w + x) * 4
            out[oi : oi + 4] = src[si : si + 4]
    return bytes(out)


def load_png_rgba(path: str) -> tuple[int, int, bytes]:
    import binascii

    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not PNG")
    pos = 8
    width = height = 0
    raw_idat = b""
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        pos += 4
        tag = data[pos : pos + 4]
        pos += 4
        chunk = data[pos : pos + length]
        pos += length + 4
        if tag == b"IHDR":
            width, height = struct.unpack(">II", chunk[:8])
        elif tag == b"IDAT":
            raw_idat += chunk
        elif tag == b"IEND":
            break
    raw = zlib.decompress(raw_idat)
    stride = width * 4 + 1
    pixels = bytearray(width * height * 4)
    off = 0
    for y in range(height):
        off += 1
        row = raw[off : off + width * 4]
        off += width * 4
        pixels[y * width * 4 : (y + 1) * width * 4] = row
    return width, height, bytes(pixels)
