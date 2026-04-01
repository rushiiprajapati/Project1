# Automated Backup & File Organizer (Python)

A Python command-line tool that backs up files from a source folder into a dated backup directory, organizes files by type, writes a backup log, and can optionally create a ZIP archive of the backup.

This project is designed to demonstrate practical Python skills for IT support, automation, and entry-level software or system administration internships. It shows file handling, directory traversal, command-line interfaces, logging, safe copying, archive creation, and basic automated testing.

---

// Table of Contents

- [Project Overview](#project-overview)
- [Why I Built This Project](#why-i-built-this-project)
- [Main Features](#main-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How the Project Works](#how-the-project-works)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Command Options](#command-options)
- [Example Commands](#example-commands)
- [Expected Output](#expected-output)
- [Testing](#testing)
- [Possible Errors and Fixes](#possible-errors-and-fixes)
- [Future Improvements](#future-improvements)
- [Resume Description](#resume-description)
- [GitHub Tips](#github-tips)
- [Author](#author)

---

# Project Overview

The **Automated Backup & File Organizer** is a Python CLI tool that:

- Scans a source directory (and all its subfolders).
- Copies files into a backup location inside a dated folder.
- Organizes copied files into category folders (Documents, Images, Code, Archives, Other).
- Writes a log file so you know what was copied and if any errors happened.
- Can optionally create a ZIP archive of the backup folder.

This project is built to be simple enough to understand but professional enough to put on your resume and GitHub profile.

---

# Why I Built This Project

I built this project to:

- Practice Python in a real-world, practical way.
- Learn how to automate common IT tasks like backups and file organization.
- Show skills that are relevant for Computer Science and IT internships (IT support, automation, system administration, basic DevOps).

It demonstrates:

- Python scripting
- File and folder operations
- Command-line tools
- Error handling and logging
- Basic automation
- Testing with `pytest`

---

# Main Features

- Recursively scans all files inside a source folder.
- Creates a **dated backup folder** for each run, e.g. `2026-03-31`.
- Organizes copied files into category folders based on file extension:
  - Documents
  - Spreadsheets
  - Images
  - Videos
  - Code
  - Archives
  - Other
- Uses **safe copy logic** to avoid overwriting existing files (adds suffix like `_1`, `_2`, etc.).
- Generates a `backup_log.txt` file for each backup run.
- Skips common folders such as:
  - `.git`
  - `__pycache__`
  - `node_modules`
- Checks available disk space before starting backup.
- Optionally creates a ZIP archive of the backup folder.
- Provides a clean command-line interface using `argparse`.
- Includes basic automated tests using `pytest`.

---

// Technologies Used

// Language

- Python 3.8+

// Standard Library Modules

- `os` – directory traversal
- `shutil` – copying files, disk usage, creating ZIP archives
- `datetime` – timestamps and dated folder names
- `argparse` – parsing command-line arguments
- `pathlib` – object-oriented path handling
- `tempfile` – temporary folders in tests

// Testing

- `pytest` – for running unit tests

---

// Project Structure

```text
py-backup-organizer/
  backup_organizer/
    __init__.py
    config.py
    backup.py
    cli.py
  tests/
    __init__.py
    test_backup.py
  README.md
  requirements.txt
```

### File Descriptions

- `backup_organizer/__init__.py`  
  Marks `backup_organizer` as a Python package and can store the package version.

- `backup_organizer/config.py`  
  Contains:
  - File type rules (which extensions go into which folder).
  - List of folder names to exclude.
  - Helper to normalize paths.

- `backup_organizer/backup.py`  
  Contains the main logic:
  - Walking the source directory
  - Checking disk space
  - Creating dated backup folders
  - Categorizing files
  - Copying files safely
  - Writing the log file
  - Optionally creating a ZIP archive

- `backup_organizer/cli.py`  
  Contains the command-line interface:
  - Defines CLI options with `argparse`
  - Calls `backup_and_organize()` with parsed arguments

- `tests/test_backup.py`  
  Contains `pytest` tests using temporary directories to verify:
  - Backup folder creation
  - File copying and categorization
  - Excluded folders are ignored
  - Unknown extensions go to `Other`

- `requirements.txt`  
  Lists Python dependencies (e.g. `pytest`).

- `README.md`  
  The file you are reading now.

---

# How the Project Works

1. **Input from user**:  
   You provide:
   - `--source`: the folder you want to back up  
   - `--backup-root`: where backups should be stored

2. **Validation**:  
   The script checks that the source folder exists and creates the backup root folder if needed.

3. **Disk space check**:  
   It estimates how much data will be copied and checks if there is enough free space in the backup destination.

4. **Create dated folder**:  
   It creates a folder like `YYYY-MM-DD` (e.g. `2026-03-31`) inside the backup root.

5. **Scan and categorize**:  
   It walks through the source folder (recursively), skipping excluded folders. For each file:
   - Looks at the file extension.
   - Chooses a category (Documents, Images, etc.).
   - Decides the destination folder inside the dated backup.

6. **Safe copy**:  
   Copies the file to the destination:
   - If the file name already exists, it adds `_1`, `_2`, etc., to avoid overwriting.

7. **Logging**:  
   Records all operations in a list, including:
   - COPIED lines (source → destination)
   - ERROR lines (if any error occurred)

8. **Log file**:  
   Unless `--no-log` is used, it writes everything to `backup_log.txt` in the dated folder.

9. **ZIP archive** (optional):  
   If `--zip` is used, after copying it creates a `.zip` archive of the dated backup folder.

---

// Installation

# 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/py-backup-organizer.git
cd py-backup-organizer
```

Replace `YOUR-USERNAME` with your GitHub username.

# 2. Create a virtual environment (optional but recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

# 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# How to Run

From the project root (`py-backup-organizer`), run:

```bash
python -m backup_organizer.cli --source "C:/Users/You/Documents" --backup-root "D:/Backups" --zip
```

- Change the paths to folders that exist on your system.
- Remove `--zip` if you do not want a ZIP archive.

---

# Command Options

| Option           | Short | Required | Description                                                      |
|------------------|-------|----------|------------------------------------------------------------------|
| `--source`       | `-s`  | Yes      | Path to the source folder to back up                            |
| `--backup-root`  | `-b`  | Yes      | Path to the backup root folder (dated folder is created inside) |
| `--zip`          | —     | No       | If present, creates a ZIP file of the backup folder             |
| `--no-log`       | —     | No       | If present, does not write `backup_log.txt`                     |

---

// Example Commands

# Basic backup

```bash
python -m backup_organizer.cli --source "C:/Users/Rushi/Documents" --backup-root "D:/MyBackups"
```

# Backup with ZIP archive

```bash
python -m backup_organizer.cli --source "C:/Users/Rushi/Documents" --backup-root "D:/MyBackups" --zip
```

# Backup without log file

```bash
python -m backup_organizer.cli --source "C:/Users/Rushi/Documents" --backup-root "D:/MyBackups" --no-log
```

---

// Expected Output

# Terminal output

On success, you might see:

```text
Files copied: 27, Errors: 0
Created ZIP archive: D:\MyBackups\2026-03-31.zip
```

On error, you might see:

```text
Backup failed: Source folder 'C:\Bad\Path' is not valid
```

or

```text
Backup failed: Not enough free space on backup drive. Aborting backup.
```

### Backup folder structure

If your backup root is `D:/MyBackups`, after running you might have:

```text
D:/MyBackups/
  2026-03-31/
    Documents/
    Images/
    Code/
    Archives/
    Other/
    backup_log.txt
  2026-03-31.zip   (only if you used --zip)
```

# Log file contents (`backup_log.txt`)

Example log:

```text
Backup run: 2026-03-31 14:10:32
Source: C:\Users\Rushi\Documents
Backup folder: D:\MyBackups\2026-03-31

COPIED: C:\Users\Rushi\Documents\resume.pdf -> D:\MyBackups\2026-03-31\Documents\resume.pdf
COPIED: C:\Users\Rushi\Documents\photo.jpg -> D:\MyBackups\2026-03-31\Images\photo.jpg

Files copied: 27, Errors: 0
```

---

# Testing

The project includes simple tests using `pytest`.

### Install test dependency

If you haven’t already:

```bash
pip install -r requirements.txt
```

### Run all tests

From the project root:

```bash
pytest
```

or:

```bash
python -m pytest
```

# What the tests do

- Create temporary folders and dummy files.
- Run `backup_and_organize()` against those folders.
- Check that:
  - A dated folder is created.
  - Files are copied into the correct category folders.
  - A `backup_log.txt` file exists.
  - Excluded folders (like `.git`) are not copied.
  - Unknown file types go to the `Other` category.

---

## Possible Errors and Fixes

### 1. `Source folder 'X' is not valid`

**Cause:**  
The `--source` path does not exist or is typed incorrectly.

**Fix:**  
- Double-check the path.
- Make sure you put the path in quotes if it contains spaces.

---

### 2. `Not enough free space on backup drive. Aborting backup.`

**Cause:**  
The backup destination drive does not have enough free space.

**Fix:**  
- Delete or move some files from the backup drive.
- Choose a different `--backup-root` location.

---

# 3. No files copied

**Possible causes:**

- The source folder is empty.
- All content is inside excluded folders.

**Fix:**

- Check the contents of the source folder.
- Open `config.py` and review the `EXCLUDED_FOLDERS` set.

---

# 4. ZIP file not created

**Cause:**  
You did not include the `--zip` flag.

**Fix:**  
Run the command again and add `--zip`.

---

# Author :
Rushi Prajapati 
Lethbridge, Alberta, Canada  
`rushi28prajapati@gmail.com`
