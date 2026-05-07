import sys
import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from _bootstrap import SRC_DIR  # noqa: F401
from automation_task_script import cli


class CLITests(unittest.TestCase):
    def test_cli_success(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "invoice.pdf").write_text("content", encoding="utf-8")
            stdout = StringIO()
            stderr = StringIO()

            with patch.object(sys, "argv", ["automation-task-script", str(root)]):
                with patch("sys.stdout", stdout), patch("sys.stderr", stderr):
                    exit_code = cli.main()

            self.assertEqual(exit_code, 0)
            self.assertIn("Organizacion completada.", stdout.getvalue())
            self.assertIn("- Documentos: 1", stdout.getvalue())
            self.assertEqual("", stderr.getvalue())

    def test_build_parser_defaults_to_current_directory(self) -> None:
        parser = cli.build_parser()
        args = parser.parse_args([])
        self.assertEqual(args.directory, ".")


if __name__ == "__main__":
    unittest.main()
