# backup_organizer/backup.py

import os
import shutil
import datetime
from pathlib import Path

from .config import FILE_RULES, EXCLUDED_FOLDERS, normalize_path


def get_category(extension: str) -> str:
    ext = extension.lower()
    for folder_name, exts in FILE_RULES.items():
        if ext in exts:
            return folder_name
    return "Other"


def create_backup_folder(backup_root: Path) -> Path:
    today = datetime.date.today()
    folder_name = today.strftime("%Y-%m-%d")
    backup_folder = backup_root / folder_name
    backup_folder.mkdir(parents=True, exist_ok=True)
    return backup_folder


def safe_copy(src: Path, dest_folder: Path) -> Path:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest = dest_folder / src.name
    counter = 1
    while dest.exists():
        dest = dest_folder / f"{src.stem}_{counter}{src.suffix}"
        counter += 1
    shutil.copy2(src, dest)
    return dest


def estimate_source_size(src_folder: Path) -> int:
    total_size = 0
    for root, dirs, files in os.walk(src_folder):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        for name in files:
            file_path = Path(root) / name
            try:
                total_size += file_path.stat().st_size
            except OSError:
                continue
    return total_size


def enough_space_available(src_folder: Path, backup_root: Path, min_free_ratio: float = 0.1) -> bool:
    total_size = estimate_source_size(src_folder)
    usage = shutil.disk_usage(backup_root)
    free_space = usage.free
    return free_space >= total_size * (1 + min_free_ratio)


def backup_and_organize(
    source_folder: str,
    backup_root: str,
    make_zip: bool = False,
    no_log: bool = False,
) -> Path:
    src = normalize_path(source_folder)
    backup_root_path = normalize_path(backup_root)

    if not src.is_dir():
        raise ValueError(f"Source folder '{src}' is not valid")

    backup_root_path.mkdir(parents=True, exist_ok=True)

    if not enough_space_available(src, backup_root_path):
        raise RuntimeError("Not enough free space on backup drive. Aborting backup.")

    backup_folder = create_backup_folder(backup_root_path)

    log_lines = [
        f"Backup run: {datetime.datetime.now()}",
        f"Source: {src}",
        f"Backup folder: {backup_folder}",
        "",
    ]

    files_copied = 0
    errors = 0

    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        root_path = Path(root)

        for name in files:
            file_path = root_path / name
            category = get_category(file_path.suffix)
            dest_folder = backup_folder / category

            try:
                copied_path = safe_copy(file_path, dest_folder)
                log_lines.append(f"COPIED: {file_path} -> {copied_path}")
                files_copied += 1
            except Exception as e:
                log_lines.append(f"ERROR: {file_path} -> {e}")
                errors += 1

    summary = f"\nFiles copied: {files_copied}, Errors: {errors}"
    log_lines.append(summary)

    if not no_log:
        log_file = backup_folder / "backup_log.txt"
        log_file.write_text("\n".join(log_lines), encoding="utf-8")

    print(summary)

    if make_zip:
        zip_base_name = str(backup_folder)
        zip_path = shutil.make_archive(zip_base_name, "zip", root_dir=backup_folder)
        print(f"Created ZIP archive: {zip_path}")

    return backup_folder