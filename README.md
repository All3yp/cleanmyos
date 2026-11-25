# 🧹 CleanMyOS

> A fast visual system cleaner, large file analyzer, and anti-stutter optimizer for **Linux** (compatible with Ubuntu, Debian, Fedora, Arch Linux, CachyOS, openSUSE, and derivatives), inspired by **CleanMyMac**.

[![Português](https://img.shields.io/badge/Language-Português_(pt--BR)-green.svg)](README.pt-BR.md)

---

## ⚡ Features

- **Deep System & Cache Cleanup:**
  - 🗑 **Trash & Temporary:** Cleans user trash (`~/.local/share/Trash`) and thumbnail caches.
  - 💻 **Developer Caches:** Scans and cleans `pip`, `uv`, `pre-commit`, `go-build`, `pnpm`, `npm`, `cargo` (Rust), `Shelly`, `codex-runtimes`, and VS Code extension caches.
  - 🌐 **Web Browsers:** Microsoft Edge, Waterfox, Firefox, Google Chrome, and Brave.
  - 📦 **Package Managers (Multi-Distro):**
    - **Ubuntu / Debian / Mint:** Cleans `apt` caches (`apt-get clean` / `autoremove`).
    - **Arch / CachyOS / Manjaro:** Cleans `pacman` and `yay` caches keeping safe rollbacks.
    - **Fedora / RHEL:** Cleans `dnf` cache (`dnf clean all`).
    - **openSUSE:** Cleans `zypper` cache.
    - **Flatpak:** Uninstalls orphaned runtimes.
  - 🐳 **Docker / Podman:** Cleans build caches and stopped containers.
  - 📋 **Logs & Crash Dumps:** Vacuums accumulated `journalctl` logs and removes system coredumps.

- **📁 Large Files Finder:**
  - Quickly scans target folders (`Downloads`, `Videos`, `Documents`, `Desktop`) and lists the largest files (> 500 MB) in a clean terminal table.

- **🚀 Anti-Stutter & Performance Diagnostics:**
  - **Hybrid / Dedicated GPU:** Alerts when NVIDIA dGPU is idling at 16W+ and allows switching to Integrated mode via `supergfxctl`.
  - **Ananicy-CPP:** Verifies real-time process priority rules (prevents micro-stutters for games and audio).
  - **NVMe TRIM:** Checks periodic SSD maintenance status.

- **🌐 Multilingual Support (i18n):**
  - Switch between English (en-US) and Portuguese (pt-BR) anytime during installation, via CLI flag (`--lang en|pt`), or from the interactive menu.

- **🛡 Safety First:**
  - Typing `cleanmyos` or `clean` by itself displays the help guide without touching any files.

---

## 📦 Installation

The installer automatically detects your Linux distribution and shell (**Fish**, **Zsh**, or **Bash**), configuring your PATH and language preference:

### Option 1: Via Install Script (Recommended)
```bash
git clone https://github.com/.../cleanmyos.git
cd cleanmyos
chmod +x install.sh
./install.sh
```
*During installation, it will ask for your preferred language (Portuguese or English).*

To run unattended in English:
```bash
./install.sh --lang=en
```

### Option 2: Self-Install via Python
```bash
python3 cleanmyos --install
```

### Option 3: Run with uv (using `pyproject.toml`)
If you prefer using [uv](https://docs.astral.sh/uv/getting-started/installation/), you can run or install the project directly:

```bash
# Run without installing globally
uv run --with rich python cleanmyos -i

# Or install as a tool from the local project
uv tool install .
cleanmyos -i
```

---

## 💻 Usage

### 1. Interactive Dashboard (CleanMyMac style)
```bash
cleanmyos -i
# or
clean -i
```

### 2. Quick Diagnostics Scan (Dry run)
```bash
cleanmyos -s
```

### 3. List Large Files (> 500 MB)
```bash
cleanmyos -l
```

### 4. Automatic Safe Cleanup
```bash
cleanmyos -y
```

### 5. Change Language
```bash
cleanmyos --lang en   # English
cleanmyos --lang pt   # Portuguese
```

### 6. Update CleanMyOS
Fetches updates directly from the original upstream repository (even if using a fork) and reinstalls automatically:
```bash
cleanmyos --update
# or from the repo:
./update.sh
```

### 7. Help
```bash
cleanmyos -h
```

---

## 🛠 Requirements
- Any Linux distribution (Ubuntu, Debian, Fedora, Arch, openSUSE, etc.)
- Python 3.9+
- `rich` Python package (installed automatically by `install.sh`)
- Optional: [uv](https://docs.astral.sh/uv/getting-started/installation/) for running/installing via `pyproject.toml`

---

## 🧪 Running tests

The project uses Python's built-in `unittest` (no extra dependencies required to run the current suite).

```bash
python3 -m unittest discover -s tests -v
```

If you want to use `pytest` (optional dev dependency):

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest -v
```

---

## 🧭 Uninstallation
To remove from your system:
```bash
./uninstall.sh
```
