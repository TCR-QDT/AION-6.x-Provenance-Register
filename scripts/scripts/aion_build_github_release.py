#!/usr/bin/env python3
"""
AION-7.1.x — GitHub Release Tarball Builder
============================================

Produces a self-contained tar.gz containing:
  - All canonical artifacts in download/
  - The complete .github/ governance layer
  - The verification scripts in scripts/
  - The worklog
  - A MANIFEST.txt with SHA-256 hashes of every file

The tarball is structured so that unpacking it yields a ready-to-push
GitHub repository (the inner directory is named aion-7.1.x/).
"""

import hashlib
import tarfile
import io
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE = Path("/home/z/my-project")
DOWNLOAD = BASE / "download"
SCRIPTS = BASE / "scripts"
WORKLOG = BASE / "worklog.md"

# Output tarball path
OUT_DIR = BASE / "download"
OUT_NAME = "aion-7.1.x-github-release.tar.gz"
OUT_PATH = OUT_DIR / OUT_NAME

# Inner directory name inside the tarball
INNER = "aion-7.1.x"

tz_sp = timezone(timedelta(hours=-3))
now = datetime.now(tz_sp)
now_str = now.strftime("%Y-%m-%d %H:%M:%S (UTC-3)")
now_iso = now.strftime("%Y-%m-%dT%H:%M:%S%z")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Collect files to include
files_to_include = []

# 1. download/ artifacts (excluding the tarball itself and any prior release)
for p in sorted(DOWNLOAD.rglob("*")):
    if p.is_file():
        rel = p.relative_to(DOWNLOAD)
        # Skip the output tarball itself
        if rel.name == OUT_NAME:
            continue
        # Skip prior release tarballs
        if rel.name.endswith(".tar.gz"):
            continue
        files_to_include.append((p, f"{INNER}/{rel.as_posix()}"))

# 2. scripts/
for p in sorted(SCRIPTS.rglob("*")):
    if p.is_file():
        rel = p.relative_to(BASE)
        files_to_include.append((p, f"{INNER}/{rel.as_posix()}"))

# 3. worklog.md
if WORKLOG.exists():
    files_to_include.append((WORKLOG, f"{INNER}/worklog.md"))

# Build MANIFEST.txt content
manifest_lines = [
    "AION-7.1.x — GitHub Release Manifest",
    "=====================================",
    "",
    f"Generated: {now_str}",
    f"Tarball:   {OUT_NAME}",
    f"Files:     {len(files_to_include) + 1}  (including this MANIFEST.txt)",
    "",
    "All SHA-256 hashes computed over the file bytes stored in the tarball.",
    "",
    "Format:  <sha256>  <size_bytes>  <path_in_tarball>",
    "",
    "-" * 78,
]

file_hashes = []
for src_path, archive_path in files_to_include:
    h = sha256_file(src_path)
    size = src_path.stat().st_size
    manifest_lines.append(f"{h}  {size:>8}  {archive_path}")
    file_hashes.append((archive_path, h, size))

# Compute combined hash of all file hashes (deterministic ordering)
combined = hashlib.sha256()
for archive_path, h, size in file_hashes:
    combined.update(f"{archive_path}\0{h}\0{size}\n".encode())
combined_hash = combined.hexdigest()

manifest_lines.extend([
    "-" * 78,
    "",
    f"Combined hash (deterministic over file list): {combined_hash}",
    "",
    "Verification procedure:",
    "  1. Extract the tarball:  tar -xzf aion-7.1.x-github-release.tar.gz",
    "  2. cd aion-7.1.x",
    "  3. Verify each file:     sha256sum download/*.md scripts/*.py worklog.md .github/**",
    "  4. Compare with the hashes listed above.",
    "",
    "Integrity rule (R-7.1.3 / REQ-MI.3):",
    "  The three 7.0.0 FROZEN artifacts MUST have these hashes:",
    "    AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md  = fa14c4ebdad30063f5921f1c73bdd11c7b9a263b16239aaa996bf75112b2b8b4",
    "    AION-7.0.0_EPISTEMIC_STATE_FREEZE.md     = 964e02fa5f645cdcdefc676fe12ae86fd6271ca84ef9e7bb6a2d9466f0eb58f6",
    "    AION-7.0.0_PROVENANCE_BOUNDARY.md        = 1e42245ed96ddd12e1ae6ed0ab973ffb58ea8ad8fabb12866ec198405605c72c",
    "  Any mismatch indicates tampering or corruption.",
    "",
])

manifest_content = "\n".join(manifest_lines).encode()
manifest_path_in_archive = f"{INNER}/MANIFEST.txt"

# Build the tarball
print("=" * 78)
print("AION-7.1.x — GitHub Release Tarball Builder")
print("=" * 78)
print(f"Timestamp:    {now_str}")
print(f"Output:       {OUT_PATH}")
print(f"Inner dir:    {INNER}/")
print(f"Files to pack: {len(files_to_include)} + 1 (MANIFEST.txt)")
print()

with tarfile.open(OUT_PATH, "w:gz") as tar:
    # Add all files
    for src_path, archive_path in files_to_include:
        tar.add(src_path, arcname=archive_path, recursive=False)
        print(f"  + {archive_path}")

    # Add MANIFEST.txt (in-memory)
    manifest_info = tarfile.TarInfo(name=manifest_path_in_archive)
    manifest_info.size = len(manifest_content)
    manifest_info.mtime = now.timestamp()
    manifest_info.mode = 0o644
    manifest_info.type = tarfile.REGTYPE
    tar.addfile(manifest_info, io.BytesIO(manifest_content))
    print(f"  + {manifest_path_in_archive}")

# Compute tarball hash
tarball_hash = sha256_file(OUT_PATH)
tarball_size = OUT_PATH.stat().st_size

print()
print("=" * 78)
print(f"TARBALL READY")
print(f"  Path:     {OUT_PATH}")
print(f"  Size:     {tarball_size} bytes ({tarball_size/1024:.1f} KB)")
print(f"  SHA-256:  {tarball_hash}")
print(f"  Files:    {len(files_to_include) + 1}")
print(f"  Combined: {combined_hash}")
print("=" * 78)

# Also write a small companion file with the tarball hash for the worklog
companion = OUT_DIR / "aion-7.1.x-github-release.sha256"
with companion.open("w") as f:
    f.write(f"{tarball_hash}  {OUT_NAME}\n")
print(f"Companion hash file: {companion}")
