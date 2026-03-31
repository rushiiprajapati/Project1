# tests/test_backup.py

import os
from pathlib import Path
import tempfile

from backup_organizer.backup import backup_and_organize
from backup_organizer.config import FILE_RULES, EXCLUDED_FOLDERS


def create_dummy_files(base: Path) -> None:
    """Create a small set of dummy files for testing."""
    # Documents
    (base / "doc1.txt").write_text("Hello", encoding="utf-8")
    (base / "report.pdf").write_text("PDF content", encoding="utf-8")
    # Images
    (base / "photo.jpg").write_bytes(b"\x00\x01\x02")
    # Code
    (base / "script.py").write_text("print('hi')", encoding="utf-8")
    # Folder that should be excluded
    excluded = base / ".git"
    excluded.mkdir()
    (excluded / "ignored.txt").write_text("should not be backed up", encoding="utf-8")


def test_backup_creates_dated_folder_and_copies_files():
    with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as backup_root:
        src_path = Path(src_dir)
        backup_root_path = Path(backup_root)

        create_dummy_files(src_path)

        backup_folder = backup_and_organize(
            source_folder=str(src_path),
            backup_root=str(backup_root_path),
            make_zip=False,
            no_log=False,
        )

        # Check that dated folder exists and is inside backup_root
        assert backup_folder.parent == backup_root_path
        assert backup_folder.is_dir()

        # Check that log file exists
        log_file = backup_folder / "backup_log.txt"
        assert log_file.is_file()

        # Check that some expected category folders exist and contain files
        documents_folder = backup_folder / "Documents"
        images_folder = backup_folder / "Images"
        code_folder = backup_folder / "Code"

        assert documents_folder.is_dir()
        assert images_folder.is_dir()
        assert code_folder.is_dir()

        # There should be at least one file in each of these
        assert any(documents_folder.iterdir())
        assert any(images_folder.iterdir())
        assert any(code_folder.iterdir())

        # Ensure excluded folder contents were not copied directly by name
        for root, dirs, files in os.walk(backup_folder):
            assert ".git" not in dirs


def test_excluded_folders_not_modified():
    # Simple check that EXCLUDED_FOLDERS is not empty and contains '.git'
    assert ".git" in EXCLUDED_FOLDERS
    assert len(EXCLUDED_FOLDERS) >= 1


def test_file_rules_have_default_other_category():
    # Ensure that an unknown extension goes to "Other"
    from backup_organizer.backup import get_category

    assert get_category(".unknownext") == "Other"