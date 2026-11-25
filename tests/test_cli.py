"""CLI and integration-style tests for cleanmyos."""

import contextlib
import io
import importlib.util
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "cleanmyos"
if "cleanmyos_mod" not in sys.modules:
    loader = SourceFileLoader("cleanmyos_mod", str(SCRIPT))
    spec = importlib.util.spec_from_loader("cleanmyos_mod", loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cleanmyos_mod"] = mod
    loader.exec_module(mod)
m = sys.modules["cleanmyos_mod"]


class TestCLI(unittest.TestCase):
    def test_print_help_does_not_raise(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            m.print_help("en_US")
        self.assertIn("CleanMyOS", buf.getvalue())

    def test_main_no_args_prints_help(self):
        old_argv = sys.argv
        try:
            sys.argv = ["cleanmyos"]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                m.main()
            self.assertIn("CleanMyOS", buf.getvalue())
        finally:
            sys.argv = old_argv

    def test_main_unknown_option(self):
        old_argv = sys.argv
        try:
            sys.argv = ["cleanmyos", "--wat"]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                m.main()
            out = buf.getvalue().lower()
            self.assertTrue("wat" in out or "unknown" in out or "desconhecida" in out)
        finally:
            sys.argv = old_argv

    def test_main_help_flag(self):
        old_argv = sys.argv
        try:
            sys.argv = ["cleanmyos", "-h"]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                m.main()
            self.assertIn("CleanMyOS", buf.getvalue())
        finally:
            sys.argv = old_argv

    def test_main_lang_flag_persists(self):
        import tempfile
        old_argv = sys.argv
        old_cf, old_cd = m.CONFIG_FILE, m.CONFIG_DIR
        try:
            with tempfile.TemporaryDirectory() as td:
                tmp = Path(td)
                m.CONFIG_FILE = tmp / "config.json"
                m.CONFIG_DIR = tmp
                sys.argv = ["cleanmyos", "--lang", "en", "-h"]
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    m.main()
                self.assertTrue(m.CONFIG_FILE.exists())
        finally:
            sys.argv = old_argv
            m.CONFIG_FILE, m.CONFIG_DIR = old_cf, old_cd


if __name__ == "__main__":
    unittest.main()
