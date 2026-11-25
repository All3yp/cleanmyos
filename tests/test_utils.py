"""Unit tests for utility functions in cleanmyos."""

import importlib.util
import os
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


class TestFormatSize(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(m.format_size(0), "0.0 B")
        self.assertEqual(m.format_size(512), "512.0 B")

    def test_kilobytes(self):
        self.assertEqual(m.format_size(1024), "1.0 KB")
        self.assertEqual(m.format_size(1536), "1.5 KB")

    def test_megabytes(self):
        self.assertEqual(m.format_size(1024 * 1024), "1.0 MB")

    def test_gigabytes(self):
        self.assertEqual(m.format_size(1024 ** 3), "1.0 GB")

    def test_terabytes(self):
        self.assertEqual(m.format_size(1024 ** 4), "1.0 TB")


class TestGetDirSize(unittest.TestCase):
    def test_nonexistent_path(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(m.get_dir_size(Path(td) / "missing"), 0)

    def test_empty_dir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(m.get_dir_size(Path(td)), 0)

    def test_dir_with_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "a.txt").write_bytes(b"a" * 100)
            (p / "b.txt").write_bytes(b"b" * 200)
            self.assertGreaterEqual(m.get_dir_size(p), 300)

    def test_nested_dirs(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            sub = p / "sub"
            sub.mkdir()
            (sub / "c.txt").write_bytes(b"c" * 50)
            self.assertGreaterEqual(m.get_dir_size(p), 50)


class TestLocales(unittest.TestCase):
    def test_get_locales_dir_exists(self):
        self.assertTrue(m.get_locales_dir().exists())

    def test_load_locale_strings_pt(self):
        strings = m.load_locale_strings("pt_BR")
        self.assertIsInstance(strings, dict)
        self.assertIn("title", strings)
        self.assertIn("menu_0", strings)

    def test_load_locale_strings_en(self):
        strings = m.load_locale_strings("en_US")
        self.assertIsInstance(strings, dict)
        self.assertTrue(strings.get("title"))

    def test_load_locale_strings_fallback(self):
        strings = m.load_locale_strings("nonexistent")
        self.assertIsInstance(strings, dict)


class TestLangPreference(unittest.TestCase):
    def test_save_and_load(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            config_file = tmp / "config.json"
            old_cf, old_cd = m.CONFIG_FILE, m.CONFIG_DIR
            try:
                m.CONFIG_FILE = config_file
                m.CONFIG_DIR = tmp
                m.save_lang_preference("en_US")
                self.assertTrue(config_file.exists())
                self.assertEqual(m.load_lang_preference(), "en_US")
                m.save_lang_preference("pt_BR")
                self.assertEqual(m.load_lang_preference(), "pt_BR")
            finally:
                m.CONFIG_FILE, m.CONFIG_DIR = old_cf, old_cd

    def test_load_invalid_defaults(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            config_file = tmp / "config.json"
            config_file.write_text("not json", encoding="utf-8")
            old_cf = m.CONFIG_FILE
            old_lang = os.environ.get("LANG")
            try:
                m.CONFIG_FILE = config_file
                os.environ["LANG"] = "en_US.UTF-8"
                self.assertEqual(m.load_lang_preference(), "en_US")
            finally:
                m.CONFIG_FILE = old_cf
                if old_lang is None:
                    os.environ.pop("LANG", None)
                else:
                    os.environ["LANG"] = old_lang

    def test_load_missing_uses_env(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            old_cf = m.CONFIG_FILE
            old_lang = os.environ.get("LANG")
            try:
                m.CONFIG_FILE = Path(td) / "missing.json"
                os.environ["LANG"] = "pt_BR.UTF-8"
                self.assertEqual(m.load_lang_preference(), "pt_BR")
            finally:
                m.CONFIG_FILE = old_cf
                if old_lang is None:
                    os.environ.pop("LANG", None)
                else:
                    os.environ["LANG"] = old_lang


class TestGetDistroInfo(unittest.TestCase):
    def test_returns_tuple(self):
        name, pkg, cache = m.get_distro_info()
        self.assertIsInstance(name, str)
        self.assertIsInstance(pkg, str)
        self.assertIn(pkg, {"pacman", "apt", "dnf", "zypper", "generic"})
        self.assertTrue(cache is None or isinstance(cache, Path))


if __name__ == "__main__":
    unittest.main()
