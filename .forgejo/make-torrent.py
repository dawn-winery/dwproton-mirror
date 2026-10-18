#!/usr/bin/env python3

import hashlib
import os
import sys
import time

BLOCK_SIZE   = 16 * 1024
PIECE_LENGTH = 256 * 1024
ZERO_HASH    = b"\x00" * 32

def bencode(obj):
    """Encode an int/bytes/list/dict as bencode; dict keys must be bytes."""
    if isinstance(obj, int):
        return b"i" + str(obj).encode() + b"e"

    if isinstance(obj, bytes):
        return str(len(obj)).encode() + b":" + obj

    if isinstance(obj, (list, tuple)):
        return b"l" + b"".join(bencode(item) for item in obj) + b"e"

    if isinstance(obj, dict):
        return (b"d"
                + b"".join(bencode(key) + bencode(obj[key]) for key in sorted(obj))
                + b"e")

    raise TypeError(f"not bencodable: {type(obj)!r}")

def merkle_root(hashes):
    """Root of a binary merkle tree; len(hashes) must be a power of two."""
    while len(hashes) > 1:
        hashes = [
            hashlib.sha256(hashes[i] + hashes[i + 1]).digest()
            for i in range(0, len(hashes), 2)
        ]

    return hashes[0]

def hash_file(path):
    """Return (v1 piece hashes, v2 piece layer hashes, length) for a file."""
    blocks_per_piece = PIECE_LENGTH // BLOCK_SIZE

    v1_pieces = []
    v2_pieces = []

    length = 0

    with open(path, "rb") as f:
        while True:
            chunk = f.read(PIECE_LENGTH)

            if not chunk:
                break

            length += len(chunk)

            v1_pieces.append(hashlib.sha1(chunk).digest())

            blocks = [
                hashlib.sha256(chunk[i : i + BLOCK_SIZE]).digest()
                for i in range(0, len(chunk), BLOCK_SIZE)
            ]

            if len(blocks) < blocks_per_piece:
                # The last (partial) piece is padded to the piece boundary.
                # If the whole file fits in a single piece it is padded to the
                # next power of two instead (BEP 52).
                required = (
                    1 << (len(blocks) - 1).bit_length()
                    if not v2_pieces
                    else blocks_per_piece
                )

                blocks.extend([ZERO_HASH] * (required - len(blocks)))

            v2_pieces.append(merkle_root(blocks))

    return v1_pieces, v2_pieces, length

def build(path):
    """Return the metainfo dictionary and the v1/v2 info dictionaries."""
    name = os.path.basename(path)
    tag = name.removesuffix("-x86_64.tar.xz")

    assert tag != name, name

    asset_url = f"https://git.dawn.wine/dawn-winery/dwproton/releases/download/{tag}/{name}"
    comment_url = f"https://git.dawn.wine/dawn-winery/dwproton/releases/tag/{tag}"

    v1_pieces, v2_pieces, length = hash_file(path)

    # The piece layer is stored as-is, while the merkle tree it belongs to is
    # balanced with the root of an all-zero piece before computing the root.
    layer = list(v2_pieces)

    if len(layer) > 1:
        pad_piece = merkle_root([ZERO_HASH] * (PIECE_LENGTH // BLOCK_SIZE))
        size = 1 << (len(layer) - 1).bit_length()

        layer.extend([pad_piece] * (size - len(layer)))

    pieces_root = merkle_root(layer)

    info = {
        b"attr": b"x",
        b"file tree": {
            name.encode(): {
                b"": {
                    b"attr": b"x",
                    b"length": length,
                    b"pieces root": pieces_root,
                }
            }
        },
        b"length": length,
        b"meta version": 2,
        b"name": name.encode(),
        b"piece length": PIECE_LENGTH,
        b"pieces": b"".join(v1_pieces),
    }

    meta = {
        b"comment": comment_url.encode(),
        b"creation date": int(time.time()),
        b"info": info,
        b"url-list": [asset_url.encode()],
    }

    # A piece layer entry is required only for files spanning multiple pieces.
    if len(v2_pieces) > 1:
        meta[b"piece layers"] = {
            pieces_root: b"".join(v2_pieces)
        }

    return info, meta


def magnet_link(info, meta):
    """Build the magnet link matching the created torrent."""
    name = info[b"name"].decode()
    length = info[b"length"]
    seed = meta[b"url-list"][0].decode()

    return "&".join([
        f"magnet:?xt=urn:btih:{hashlib.sha1(bencode(info)).hexdigest()}",
        f"xt=urn:btmh:1220{hashlib.sha256(bencode(info)).hexdigest()}",
        f"dn={name}",
        f"xl={length}",
        f"ws={seed}",
    ])


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {os.path.basename(sys.argv[0])} ARCHIVE")

    archive = sys.argv[1]

    if not os.path.isfile(archive):
        sys.exit(f"error: {archive}: not a regular file")

    info, meta = build(archive)

    with open(archive + ".torrent", "wb") as f:
        f.write(bencode(meta))

    print(magnet_link(info, meta))

if __name__ == "__main__":
    main()
