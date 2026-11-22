import hashlib
from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader

LOADERS = {".txt": TextLoader, ".pdf": PyPDFLoader, ".docx": Docx2txtLoader}


def _files_keeping_first_copy(
    data_dir: Path,
) -> tuple[list[Path], list[tuple[str, str]]]:
    """Return supported files, keeping only the first of any identical files."""
    candidates = [
        path
        for path in data_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in LOADERS
        and path.stat().st_size > 0
    ]
    candidates.sort(key=lambda path: path.name.lower())

    files = []
    duplicates = []
    seen_hashes: dict[str, str] = {}
    for path in candidates:
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        original_name = seen_hashes.get(file_hash)
        if original_name is not None:
            duplicates.append((path.name, original_name))
            continue
        seen_hashes[file_hash] = path.name
        files.append(path)
    return files, duplicates


def _supported_files(data_dir: Path) -> tuple[list[Path], list[str]]:
    """Return the files we keep, and a warning for each later copy."""
    files, duplicates = _files_keeping_first_copy(data_dir)
    warnings = []
    for duplicate_name, original_name in duplicates:
        warnings.append(f"Skipped duplicate of {original_name}: {duplicate_name}")
    return files, warnings
