"""Unit tests for CleanMyOS class behavior."""

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


def make_app(tmp_path, monkeypatch_lang="en_US"):
    old_home, old_cd, old_cf = m.HOME, m.CONFIG_DIR, m.CONFIG_FILE
    old_distro = m.get_distro_info
    m.HOME = tmp_path
    m.CONFIG_DIR = tmp_path / ".config/cleanmyos"
    m.CONFIG_FILE = tmp_path / ".config/cleanmyos/config.json"
    m.get_distro_info = lambda: ("TestLinux", "apt", tmp_path / "pkgcache")
    app = m.CleanMyOS(lang=monkeypatch_lang)
    return app, (old_home, old_cd, old_cf, old_distro)


def restore(state):
    m.HOME, m.CONFIG_DIR, m.CONFIG_FILE, m.get_distro_info = state


class TestCleanMyOSInit(unittest.TestCase):
    def test_init_sets_language(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            app, st = make_app(Path(td), "pt_BR")
            try:
                self.assertEqual(app.lang, "pt_BR")
                self.assertEqual(app.distro_name, "TestLinux")
                self.assertEqual(app.pkg_manager, "apt")
            finally:
                restore(st)

    def test_t_returns_key_for_missing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            app, st = make_app(Path(td))
            try:
                self.assertEqual(app.t("missing_key_xyz"), "missing_key_xyz")
            finally:
                restore(st)

    def test_t_formats_kwargs(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            app, st = make_app(Path(td))
            try:
                result = app.t("checking", item="Cache")
                self.assertIn("Cache", result)
            finally:
                restore(st)


class TestScanAll(unittest.TestCase):
    def test_scan_all_populates_scanned_data(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            app, st = make_app(tmp)
            old_which, old_run = m.shutil.which, m.subprocess.run
            try:
                trash = tmp / ".local/share/Trash"
                trash.mkdir(parents=True)
                (trash / "file.txt").write_text("hello", encoding="utf-8")
                m.shutil.which = lambda cmd: None
                m.subprocess.run = lambda *a, **k: type("R", (), {"returncode": 1, "stdout": "", "stderr": ""})()
                app.scan_all()
                self.assertIn("_grand_total", app.scanned_data)
                self.assertGreaterEqual(app.scanned_data["_grand_total"], 0)
            finally:
                m.shutil.which, m.subprocess.run = old_which, old_run
                restore(st)

    def test_scan_uses_get_dir_size(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            app, st = make_app(tmp)
            old_which, old_run, old_gds = m.shutil.which, m.subprocess.run, m.get_dir_size
            try:
                m.shutil.which = lambda cmd: None
                m.subprocess.run = lambda *a, **k: type("R", (), {"returncode": 1, "stdout": ""})()
                m.get_dir_size = lambda p: 1234
                p = tmp / ".cache/pip"
                p.mkdir(parents=True)
                app.scan_all()
                self.assertGreaterEqual(app.scanned_data["_grand_total"], 1234)
            finally:
                m.shutil.which, m.subprocess.run, m.get_dir_size = old_which, old_run, old_gds
                restore(st)


class TestLargeFiles(unittest.TestCase):
    def test_scan_large_files_finds_big_file(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            app, st = make_app(tmp)
            try:
                downloads = tmp / "Downloads"
                downloads.mkdir()
                big = downloads / "big.bin"
                big.write_bytes(b"0" * (600 * 1024 * 1024))
                files = app.scan_large_files(min_size_mb=500)
                self.assertEqual(len(files), 1)
                self.assertEqual(files[0][2], "Downloads")
                self.assertGreaterEqual(files[0][1], 500 * 1024 * 1024)
            finally:
                restore(st)

    def test_scan_large_files_ignores_small(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            app, st = make_app(tmp)
            try:
                downloads = tmp / "Downloads"
                downloads.mkdir()
                (downloads / "small.bin").write_bytes(b"123")
                self.assertEqual(app.scan_large_files(min_size_mb=500), [])
            finally:
                restore(st)

    def test_scan_large_files_missing_dirs(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            app, st = make_app(Path(td))
            try:
                self.assertEqual(app.scan_large_files(min_size_mb=1), [])
            finally:
                restore(st)


class TestCleanCategory(unittest.TestCase):
    def test_clean_category_removes_dir_contents(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            app, st = make_app(tmp)
            try:
                trash = tmp / ".local/share/Trash"
                trash.mkdir(parents=True)
                f = trash / "old.txt"
                f.write_text("junk", encoding="utf-8")
                sub = trash / "folder"
                sub.mkdir()
                (sub / "nested.txt").write_text("nested", encoding="utf-8")

                app.scan_all()
                cat = app.t("cat_trash")
                freed = app.clean_category(cat)

                self.assertFalse(f.exists())
                self.assertFalse(sub.exists())
                self.assertTrue(trash.exists())
                self.assertGreaterEqual(freed, 0)
            finally:
                restore(st)

    def test_clean_category_handles_missing_path(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            app, st = make_app(Path(td))
            try:
                app.scan_all()
                cat = app.t("cat_trash")
                freed = app.clean_category(cat)
                self.assertEqual(freed, 0)
            finally:
                restore(st)


if __name__ == "__main__":
    unittest.main()
