# backup_organizer/cli.py

import argparse

from .backup import backup_and_organize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automated Backup & File Organizer (Python)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source",
        "-s",
        required=True,
        help="Path to source folder to back up",
    )
    parser.add_argument(
        "--backup-root",
        "-b",
        required=True,
        help="Path to root backup folder (dated folder will be created inside)",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Create a ZIP archive of the backup folder after copying",
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Do not write backup_log.txt (only print summary)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        backup_and_organize(
            source_folder=args.source,
            backup_root=args.backup_root,
            make_zip=args.zip,
            no_log=args.no_log,
        )
    except Exception as e:
        print(f"Backup failed: {e}")


if __name__ == "__main__":
    main()