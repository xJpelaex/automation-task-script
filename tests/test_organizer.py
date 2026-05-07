import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from _bootstrap import SRC_DIR  # noqa: F401
from automation_task_script.organizer import FileOrganizer


def create_file(path: Path, content: str = "sample") -> None:
    path.write_text(content, encoding="utf-8")


class FileOrganizerTests(unittest.TestCase):
    def test_organizes_files_by_extension(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            create_file(root / "report.pdf")
            create_file(root / "photo.jpg")
            create_file(root / "sheet.csv")
            create_file(root / "notes.txt")

            result = FileOrganizer(root).organize()

            self.assertEqual(result.scanned_files, 4)
            self.assertEqual(result.moved_files, 4)
            self.assertTrue((root / "Documentos" / "report.pdf").exists())
            self.assertTrue((root / "Imágenes" / "photo.jpg").exists())
            self.assertTrue((root / "Datos" / "sheet.csv").exists())
            self.assertTrue((root / "Otros" / "notes.txt").exists())

    def test_skips_existing_directories(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            create_file(root / "archive.png")
            (root / "custom_folder").mkdir()

            result = FileOrganizer(root).organize()

            self.assertEqual(result.scanned_files, 1)
            self.assertGreaterEqual(result.skipped_entries, 1)
            self.assertTrue((root / "Imágenes" / "archive.png").exists())

    def test_renames_on_name_collision(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            create_file(root / "budget.csv")
            datos_dir = root / "Datos"
            datos_dir.mkdir()
            create_file(datos_dir / "budget.csv", "existing")

            FileOrganizer(root).organize()

            self.assertTrue((datos_dir / "budget.csv").exists())
            self.assertTrue((datos_dir / "budget_1.csv").exists())

    def test_raises_for_missing_directory(self) -> None:
        with TemporaryDirectory() as temp_dir:
            missing_dir = Path(temp_dir) / "missing"

            with self.assertRaises(FileNotFoundError):
                FileOrganizer(missing_dir).organize()


if __name__ == "__main__":
    unittest.main()
