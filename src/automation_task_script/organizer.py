"""Core file organization logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from shutil import move


@dataclass(slots=True)
class OrganizationResult:
    """Collects the outcome of an organization run."""

    scanned_files: int = 0
    moved_files: int = 0
    skipped_entries: int = 0
    errors: list[str] = field(default_factory=list)
    by_category: dict[str, int] = field(
        default_factory=lambda: {
            "Documentos": 0,
            "Imágenes": 0,
            "Datos": 0,
            "Otros": 0,
        }
    )


class FileOrganizer:
    """Organizes files in a directory using extension-based rules."""

    CATEGORY_RULES = {
        ".pdf": "Documentos",
        ".jpg": "Imágenes",
        ".jpeg": "Imágenes",
        ".png": "Imágenes",
        ".xlsx": "Datos",
        ".csv": "Datos",
    }
    FALLBACK_CATEGORY = "Otros"

    def __init__(self, target_directory: str | Path) -> None:
        self.target_directory = Path(target_directory).expanduser().resolve()

    def organize(self) -> OrganizationResult:
        result = OrganizationResult()

        if not self.target_directory.exists():
            raise FileNotFoundError(
                f"El directorio objetivo no existe: {self.target_directory}"
            )

        if not self.target_directory.is_dir():
            raise NotADirectoryError(
                f"La ruta objetivo no es una carpeta valida: {self.target_directory}"
            )

        self._ensure_destination_directories()

        for entry in self.target_directory.iterdir():
            if entry.is_dir():
                result.skipped_entries += 1
                continue

            result.scanned_files += 1
            category = self._get_category(entry)
            destination = self.target_directory / category / entry.name

            try:
                safe_destination = self._resolve_name_collision(destination)
                move(str(entry), str(safe_destination))
                result.moved_files += 1
                result.by_category[category] += 1
            except OSError as exc:
                result.errors.append(f"{entry.name}: {exc}")

        return result

    def _ensure_destination_directories(self) -> None:
        for category in {*self.CATEGORY_RULES.values(), self.FALLBACK_CATEGORY}:
            (self.target_directory / category).mkdir(exist_ok=True)

    def _get_category(self, file_path: Path) -> str:
        return self.CATEGORY_RULES.get(file_path.suffix.lower(), self.FALLBACK_CATEGORY)

    @staticmethod
    def _resolve_name_collision(destination: Path) -> Path:
        if not destination.exists():
            return destination

        counter = 1
        while True:
            candidate = destination.with_name(
                f"{destination.stem}_{counter}{destination.suffix}"
            )
            if not candidate.exists():
                return candidate
            counter += 1
