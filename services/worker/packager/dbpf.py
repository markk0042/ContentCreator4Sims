"""
Minimal DBPF reader/writer for Sims 4 .package texture replacement.
Based on DBPF v2.1 (Fogity / Sims 4 Modders Reference).
"""
from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO


DBPF_MAGIC = b"DBPF"
COMPRESSION_ZLIB = 0x5A42
COMPRESSION_NONE = 0x0000

# Sims 4 Image (PNG) resource type
RESOURCE_TYPE_PNG = 0x2F7D0006


@dataclass(frozen=True)
class ResourceKey:
    type_id: int
    group_id: int
    instance_high: int
    instance_low: int

    @property
    def instance(self) -> int:
        return (self.instance_high << 32) | self.instance_low

    def matches(self, other: "ResourceKey") -> bool:
        return (
            self.type_id == other.type_id
            and self.group_id == other.group_id
            and self.instance_high == other.instance_high
            and self.instance_low == other.instance_low
        )


@dataclass
class IndexEntry:
    key: ResourceKey
    offset: int
    compressed_size: int
    uncompressed_size: int
    compression: int
    committed: int
    extended: bool
    data: bytes


def _read_u32(f: BinaryIO) -> int:
    return struct.unpack("<I", f.read(4))[0]


def _write_u32(f: BinaryIO, v: int) -> None:
    f.write(struct.pack("<I", v))


def _resolve_index_offset(data: bytes) -> int:
    """Resolve DBPF index offset (Maxis uses 0x40 data-end or tail index block)."""
    index_offset = struct.unpack_from("<Q", data, 0x44)[0]
    if index_offset > 0 and index_offset < len(data):
        return index_offset
    data_end = struct.unpack_from("<I", data, 0x40)[0]
    if data_end > 0 and data_end < len(data):
        return data_end
    index_size = struct.unpack_from("<I", data, 0x2C)[0]
    if index_size > 0 and index_size < len(data):
        return len(data) - index_size
    short = struct.unpack_from("<I", data, 0x2C)[0]
    if short > 0 and short < len(data):
        return short
    raise ValueError("Could not locate DBPF index")


def parse_package(path: Path) -> tuple[bytes, list[IndexEntry]]:
    data = path.read_bytes()
    if data[:4] != DBPF_MAGIC:
        raise ValueError(f"Not a DBPF file: {path}")

    index_count = struct.unpack_from("<I", data, 0x24)[0]
    index_offset = _resolve_index_offset(data)

    flags = struct.unpack_from("<I", data, index_offset)[0]
    pos = index_offset + 4

    const_type = flags & 0x1
    const_group = flags & 0x2
    const_inst_hi = flags & 0x4

    default_type = _read_u32_from(data, pos) if const_type else None
    pos = pos + 4 if const_type else pos

    default_group = _read_u32_from(data, pos) if const_group else None
    pos = pos + 4 if const_group else pos

    default_inst_hi = _read_u32_from(data, pos) if const_inst_hi else None
    pos = pos + 4 if const_inst_hi else pos

    entries: list[IndexEntry] = []
    for _ in range(index_count):
        type_id = default_type if const_type else _read_u32_from(data, pos)
        pos += 0 if const_type else 4

        group_id = default_group if const_group else _read_u32_from(data, pos)
        pos += 0 if const_group else 4

        inst_hi = default_inst_hi if const_inst_hi else _read_u32_from(data, pos)
        pos += 0 if const_inst_hi else 4

        inst_lo = _read_u32_from(data, pos)
        pos += 4

        res_offset = _read_u32_from(data, pos)
        pos += 4

        size_field = _read_u32_from(data, pos)
        pos += 4
        compressed_size = size_field & 0x7FFFFFFF
        extended = bool(size_field & 0x80000000)

        uncompressed_size = _read_u32_from(data, pos)
        pos += 4

        compression = COMPRESSION_ZLIB
        committed = 1
        if extended:
            compression = _read_u16_from(data, pos)
            pos += 2
            committed = _read_u16_from(data, pos)
            pos += 2

        key = ResourceKey(type_id, group_id, inst_hi, inst_lo)
        raw = data[res_offset : res_offset + compressed_size]
        if compression == COMPRESSION_ZLIB:
            payload = zlib.decompress(raw)
        elif compression == COMPRESSION_NONE:
            payload = raw
        else:
            raise ValueError(f"Unsupported compression {compression:#x} for {key}")

        entries.append(
            IndexEntry(
                key=key,
                offset=res_offset,
                compressed_size=compressed_size,
                uncompressed_size=uncompressed_size,
                compression=compression,
                committed=committed,
                extended=extended,
                data=payload,
            )
        )

    header_end = min((e.offset for e in entries), default=index_offset)
    header = data[:header_end]
    return header, entries


def _read_u32_from(data: bytes, pos: int) -> int:
    return struct.unpack_from("<I", data, pos)[0]


def _read_u16_from(data: bytes, pos: int) -> int:
    return struct.unpack_from("<H", data, pos)[0]


def _compress_resource(payload: bytes) -> tuple[bytes, int]:
    if len(payload) < 128:
        return payload, COMPRESSION_NONE
    compressed = zlib.compress(payload, 9)
    if len(compressed) >= len(payload):
        return payload, COMPRESSION_NONE
    return compressed, COMPRESSION_ZLIB


def write_package(path: Path, header_prefix: bytes, entries: list[IndexEntry]) -> None:
    """Rebuild package: header + resource blobs + index (Sims 4 / Maxis layout)."""
    resource_blobs: list[bytes] = []
    new_entries: list[IndexEntry] = []

    cursor = len(header_prefix)
    for entry in entries:
        blob, compression = _compress_resource(entry.data)
        use_ext = entry.extended or compression != COMPRESSION_NONE
        new_entries.append(
            IndexEntry(
                key=entry.key,
                offset=cursor,
                compressed_size=len(blob),
                uncompressed_size=len(entry.data),
                compression=compression,
                committed=entry.committed,
                extended=use_ext,
                data=entry.data,
            )
        )
        resource_blobs.append(blob)
        cursor += len(blob)

    index_start = cursor
    flags = 0
    index_body = bytearray()
    index_body += struct.pack("<I", flags)

    for entry, blob in zip(new_entries, resource_blobs):
        index_body += struct.pack("<I", entry.key.type_id)
        index_body += struct.pack("<I", entry.key.group_id)
        index_body += struct.pack("<I", entry.key.instance_high)
        index_body += struct.pack("<I", entry.key.instance_low)
        index_body += struct.pack("<I", entry.offset)
        size_field = entry.compressed_size | (0x80000000 if entry.extended else 0)
        index_body += struct.pack("<I", size_field)
        index_body += struct.pack("<I", entry.uncompressed_size)
        if entry.extended:
            index_body += struct.pack("<H", entry.compression)
            index_body += struct.pack("<H", entry.committed)

    index_count = len(new_entries)
    index_size = len(index_body)

    header = bytearray(header_prefix)
    if len(header) < 0x50:
        header.extend(b"\x00" * (0x50 - len(header)))

    struct.pack_into("<I", header, 0x24, index_count)
    struct.pack_into("<I", header, 0x2C, index_size)
    struct.pack_into("<I", header, 0x30, 0)
    struct.pack_into("<I", header, 0x40, index_start)
    struct.pack_into("<Q", header, 0x44, 0)

    out = bytes(header) + b"".join(resource_blobs) + bytes(index_body)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out)


def patch_package_texture(
    base_package: Path,
    output_package: Path,
    target: ResourceKey,
    texture_bytes: bytes,
    *,
    extra_targets: list[ResourceKey] | None = None,
) -> None:
    targets = [target] + (extra_targets or [])
    header, entries = parse_package(base_package)
    replaced = 0
    for entry in entries:
        for t in targets:
            if entry.key.matches(t):
                entry.data = texture_bytes
                replaced += 1
                break
    if replaced == 0:
        raise ValueError(
            f"Texture resource not found in {base_package.name}: "
            f"type={target.type_id:#010x} group={target.group_id:#010x} "
            f"instance={target.instance:#018x}"
        )
    write_package(output_package, header, entries)


def patch_package_textures(
    base_package: Path,
    output_package: Path,
    targets: list[ResourceKey],
    texture_bytes: bytes,
) -> int:
    key_to_data = {k: texture_bytes for k in targets}
    return patch_package_textures_map(base_package, output_package, key_to_data)


def dds_dimensions(dds_bytes: bytes) -> tuple[int, int]:
    if len(dds_bytes) < 20 or dds_bytes[:4] != b"DDS ":
        raise ValueError("Not a DDS payload")
    height = struct.unpack_from("<I", dds_bytes, 12)[0]
    width = struct.unpack_from("<I", dds_bytes, 16)[0]
    return width, height


def patch_package_textures_map(
    base_package: Path,
    output_package: Path,
    key_to_data: dict[ResourceKey, bytes],
) -> int:
    """Patch textures; unchanged resources keep original compressed bytes from base file."""
    if not key_to_data:
        raise ValueError("No texture targets provided")

    original = base_package.read_bytes()
    header, entries = parse_package(base_package)
    target_keys = list(key_to_data.keys())
    replaced = 0

    for entry in entries:
        for key, data in key_to_data.items():
            if entry.key.matches(key):
                entry.data = data
                replaced += 1
                break

    if replaced == 0:
        raise ValueError(f"No matching textures in {base_package.name}")

    resource_blobs: list[bytes] = []
    new_entries: list[IndexEntry] = []
    cursor = len(header)

    for entry in entries:
        is_patched = any(entry.key.matches(k) for k in target_keys)
        if is_patched:
            blob, compression = _compress_resource(entry.data)
            extended = True
        else:
            blob = original[entry.offset : entry.offset + entry.compressed_size]
            compression = entry.compression
            extended = entry.extended

        new_entries.append(
            IndexEntry(
                key=entry.key,
                offset=cursor,
                compressed_size=len(blob),
                uncompressed_size=entry.uncompressed_size if not is_patched else len(entry.data),
                compression=compression,
                committed=entry.committed,
                extended=extended,
                data=entry.data,
            )
        )
        resource_blobs.append(blob)
        cursor += len(blob)

    write_package_from_entries(output_package, header, new_entries, resource_blobs)
    return replaced


def write_package_from_entries(
    path: Path,
    header_prefix: bytes,
    entries: list[IndexEntry],
    resource_blobs: list[bytes],
) -> None:
    index_start = sum(len(b) for b in resource_blobs) + len(header_prefix)
    flags = 0
    index_body = bytearray()
    index_body += struct.pack("<I", flags)

    for entry, blob in zip(entries, resource_blobs):
        index_body += struct.pack("<I", entry.key.type_id)
        index_body += struct.pack("<I", entry.key.group_id)
        index_body += struct.pack("<I", entry.key.instance_high)
        index_body += struct.pack("<I", entry.key.instance_low)
        index_body += struct.pack("<I", entry.offset)
        size_field = entry.compressed_size | (0x80000000 if entry.extended else 0)
        index_body += struct.pack("<I", size_field)
        index_body += struct.pack("<I", entry.uncompressed_size)
        if entry.extended:
            index_body += struct.pack("<H", entry.compression)
            index_body += struct.pack("<H", entry.committed)

    header = bytearray(header_prefix)
    if len(header) < 0x50:
        header.extend(b"\x00" * (0x50 - len(header)))

    struct.pack_into("<I", header, 0x24, len(entries))
    struct.pack_into("<I", header, 0x2C, len(index_body))
    struct.pack_into("<I", header, 0x30, 0)
    struct.pack_into("<I", header, 0x40, index_start)
    struct.pack_into("<Q", header, 0x44, 0)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(header) + b"".join(resource_blobs) + bytes(index_body))


def create_minimal_texture_package(
    output_package: Path,
    png_bytes: bytes,
    *,
    type_id: int = RESOURCE_TYPE_PNG,
    group_id: int = 0,
    instance: int = 0x8000000000000001,
) -> None:
    """Create a minimal valid DBPF with one PNG resource (dev / pipeline test)."""
    inst_hi = (instance >> 32) & 0xFFFFFFFF
    inst_lo = instance & 0xFFFFFFFF
    key = ResourceKey(type_id, group_id, inst_hi, inst_lo)

    header = bytearray(0x50)
    header[0:4] = DBPF_MAGIC
    struct.pack_into("<I", header, 0x04, 2)
    struct.pack_into("<I", header, 0x08, 1)

    entry = IndexEntry(
        key=key,
        offset=0x50,
        compressed_size=0,
        uncompressed_size=len(png_bytes),
        compression=COMPRESSION_ZLIB,
        committed=1,
        extended=True,
        data=png_bytes,
    )
    write_package(output_package, bytes(header), [entry])
