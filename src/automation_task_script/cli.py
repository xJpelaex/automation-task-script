"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .organizer import FileOrganizer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automation-task-script",
        description="Organiza archivos automaticamente segun su extension.",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Ruta de la carpeta a organizar. Por defecto usa el directorio actual.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        organizer = FileOrganizer(Path(args.directory))
        result = organizer.organize()
    except (FileNotFoundError, NotADirectoryError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Organizacion completada.")
    print(f"Archivos detectados: {result.scanned_files}")
    print(f"Archivos movidos: {result.moved_files}")
    print(f"Elementos omitidos: {result.skipped_entries}")

    for category, total in result.by_category.items():
        print(f"- {category}: {total}")

    if result.errors:
        print("Se detectaron errores durante el proceso:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
