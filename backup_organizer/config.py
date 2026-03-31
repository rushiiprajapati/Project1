# backup_organizer/config.py

from pathlib import Path

# File type rules: adjust or extend as you like
FILE_RULES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
}

# Folders to skip while walking
EXCLUDED_FOLDERS = {"__pycache__", ".git", "node_modules"}


def normalize_path(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()