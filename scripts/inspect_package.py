"""Inspect Sims 4 .package index and image resources."""
from __future__ import annotations

import struct
import sys
import zlib
from collections import Counter
from pathlib import Path

IMG = {
    0x2F7D0006: "PNG",
    0x34125C89: "DDS",
    0x00B2D882: "DSTImage",
    0x3BD45407: "THUM",
    0xB6C8B6A0: "LITE",
    0x5AE1C975: "BONE",
    0xC0DB5AE7: "RLE2",
}


def iter_index(data: bytes):
    index_count = struct.unpack_from("<I", data, 0x24)[0]
    index_offset = struct.unpack_from("<Q", data, 0x44)[0]
    if index_offset == 0:
        index_offset = struct.unpack_from("<I", data, 0x2C)[0]

    pos = index_offset + 4
    flags = struct.unpack_from("<I", data, index_offset)[0]
    const_type = bool(flags & 0x1)
    const_group = bool(flags & 0x2)
    const_inst_hi = bool(flags & 0x4)

    default_type = struct.unpack_from("<I", data, pos)[0] if const_type else None
    pos += 4 if const_type else 0
    default_group = struct.unpack_from("<I", data, pos)[0] if const_group else None
    pos += 4 if const_group else 0
    default_inst_hi = struct.unpack_from("<I", data, pos)[0] if const_inst_hi else None
    pos += 4 if const_inst_hi else 0

    for _ in range(index_count):
        type_id = default_type if const_type else struct.unpack_from("<I", data, pos)[0]
        pos += 0 if const_type else 4
        group_id = default_group if const_group else struct.unpack_from("<I", data, pos)[0]
        pos += 0 if const_group else 4
        inst_hi = default_inst_hi if const_inst_hi else struct.unpack_from("<I", data, pos)[0]
        pos += 0 if const_inst_hi else 4
        inst_lo = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        res_offset = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        size_field = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        compressed_size = size_field & 0x7FFFFFFF
        extended = bool(size_field & 0x80000000)
        uncompressed_size = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        compression = 0
        if extended:
            compression = struct.unpack_from("<H", data, pos)[0]
            pos += 4

        yield {
            "type_id": type_id,
            "group_id": group_id,
            "inst_hi": inst_hi,
            "inst_lo": inst_lo,
            "offset": res_offset,
            "compressed_size": compressed_size,
            "uncompressed_size": uncompressed_size,
            "compression": compression,
        }


def decompress_entry(data: bytes, ent: dict) -> bytes | None:
    raw = data[ent["offset"] : ent["offset"] + ent["compressed_size"]]
    if ent["compression"] == 0x5A42:
        try:
            return zlib.decompress(raw)
        except zlib.error:
            return None
    if ent["compression"] == 0:
        return raw
    return None


def inspect(path: Path) -> None:
    data = path.read_bytes()
    entries = list(iter_index(data))
    types = Counter(e["type_id"] for e in entries)
    print(f"File: {path.name} ({len(data)} bytes, {len(entries)} resources)\n")
    print("Resource types (top 20):")
    for t, c in types.most_common(20):
        label = IMG.get(t, "")
        print(f"  0x{t:08X}  x{c}  {label}")

    candidates = []
    for ent in entries:
        label = IMG.get(ent["type_id"])
        if not label:
            continue
        payload = decompress_entry(data, ent)
        inst = (ent["inst_hi"] << 32) | ent["inst_lo"]
        candidates.append((ent, label, payload, inst))

    print(f"\nKnown image types: {len(candidates)}")
    for ent, label, payload, inst in sorted(
        candidates, key=lambda x: -(len(x[2]) if x[2] else 0)
    ):
        ok = payload is not None
        size = len(payload) if payload else 0
        print(
            f"  {label:8} group=0x{ent['group_id']:08X} instance=0x{inst:016X} "
            f"usize={ent['uncompressed_size']} got={size} comp=0x{ent['compression']:04X}"
        )
        if ok and payload[:8] == b"\x89PNG\r\n\x1a\n":
            print("    PNG OK")
        if ok and payload[:4] == b"DDS ":
            print("    DDS OK")


if __name__ == "__main__":
    inspect(Path(sys.argv[1]))
