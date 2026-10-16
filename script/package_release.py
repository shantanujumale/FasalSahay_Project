"""Build a clean production release archive of the FasalSahay project.

Excludes:
- .env secrets and credentials
- node_modules
- virtual environments (.venv, venv)
- Python caches (__pycache__, *.pyc)
- SQLite / local test databases (*.db, *.sqlite3)
- Test caches (.pytest_cache, .coverage)
- Frontend build output (dist/)
- Temporary uploads (backend/uploads/*)
"""
from __future__ import annotations
import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ZIP_LOCAL = PROJECT_ROOT / "FasalSahay_Production_Ready.zip"
OUTPUT_ZIP_PARENT = PROJECT_ROOT.parent / "FasalSahay_Production_Ready.zip"

EXCLUDE_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    ".git",
    ".gemini",
    ".system_generated",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".sqlite3",
}

EXCLUDE_FILES = {
    ".env",
    "pmfby_dev.db",
    "test_pmfby.db",
    ".coverage",
}


def should_exclude(path: Path) -> bool:
    rel_parts = path.relative_to(PROJECT_ROOT).parts
    for part in rel_parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith(".pytest_cache"):
            return True

    # Exclude uploaded files in uploads directory (keep folder or .gitkeep)
    if "uploads" in rel_parts and path.is_file() and path.name != ".gitkeep":
        return True

    if path.name in EXCLUDE_FILES or path.name.endswith(".env"):
        return True

    if path.suffix in EXCLUDE_EXTENSIONS:
        return True

    if "FasalSahay_Production_Ready.zip" in path.name:
        return True

    return False


def create_release():
    print(f"Creating release archive from: {PROJECT_ROOT}")
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP_LOCAL, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Prune excluded directories in-place for fast traversal
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in sorted(files):
                file_path = Path(root) / file
                if should_exclude(file_path):
                    continue
                rel_path = file_path.relative_to(PROJECT_ROOT)
                # Store under root folder 'FasalSahay'
                archive_name = Path("FasalSahay") / rel_path
                zf.write(file_path, arcname=str(archive_name))
                file_count += 1
                total_uncompressed_bytes += file_path.stat().st_size

    # Also copy to parent directory for convenience
    try:
        import shutil
        shutil.copy2(OUTPUT_ZIP_LOCAL, OUTPUT_ZIP_PARENT)
        parent_saved = str(OUTPUT_ZIP_PARENT)
    except Exception as exc:
        parent_saved = f"Could not copy to parent: {exc}"

    zip_size_mb = OUTPUT_ZIP_LOCAL.stat().st_size / (1024 * 1024)
    print(f"Release ZIP created successfully:")
    print(f" - Local path:  {OUTPUT_ZIP_LOCAL}")
    print(f" - Parent path: {parent_saved}")
    print(f" - Files packaged: {file_count}")
    print(f" - Archive size:   {zip_size_mb:.2f} MB")
    print(f" - Uncompressed:   {total_uncompressed_bytes / (1024 * 1024):.2f} MB")

    # Verify integrity by listing contents
    with zipfile.ZipFile(OUTPUT_ZIP_LOCAL, "r") as zf:
        bad_file = zf.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupt file found in archive: {bad_file}")
        print("Archive integrity verified (testzip passed).")


if __name__ == "__main__":
    create_release()
