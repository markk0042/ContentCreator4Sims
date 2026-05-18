"""Extract DDS texture instance IDs from a .package for manifest.json."""
from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path


def extract_dds_instances(path: Path, *, uncompressed_size: int = 349680) -> list[str]:
    data = path.read_bytes()
    index_size = struct.unpack_from("<I", data, 0x2C)[0]
    idx = len(data) - index_size
    pos = idx + 4
    insts: list[str] = []
    count = struct.unpack_from("<I", data, 0x24)[0]
    for _ in range(count):
        t, g, ih, il, off, sf, us = struct.unpack_from("<7I", data, pos)[:7]
        pos += 28
        if sf >> 31:
            pos += 4
        cs = sf & 0x7FFFFFFF
        if off >= idx:
            continue
        raw = data[off : off + cs]
        try:
            payload = zlib.decompress(raw)
        except zlib.error:
            continue
        if payload[:4] == b"DDS " and us == uncompressed_size:
            inst = (ih << 32) | il
            insts.append(f"0x{inst:016X}")
    return insts


if __name__ == "__main__":
    pkg = Path(sys.argv[1])
    instances = extract_dds_instances(pkg)
    print(json.dumps(instances, indent=2))
