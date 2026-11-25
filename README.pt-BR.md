# 🧹 CleanMyOS

> Um otimizador de sistema, limpador de lixo e analisador de arquivos gigantes para **Linux** (compatível com Ubuntu, Debian, Fedora, Arch Linux, CachyOS, openSUSE e derivados), inspirado na interface e praticidade do **CleanMyMac**.

[![English](https://img.shields.io/badge/Language-English_(en--US)-blue.svg)](README.md)

---

## ⚡ Funcionalidades

- **Varredura Completa de Caches e Lixo:**
  - 🗑 **Lixeira & Temporários:** Limpa lixeira do usuário e cache de miniaturas (*thumbnails*).
  - 💻 **Caches de Desenvolvimento:** Varre e limpa caches de `pip`, `uv`, `pre-commit`, `go-build`, `pnpm`, `npm`, `cargo` (Rust), `Shelly`, `codex-runtimes` e extensões do VS Code.
  - 🌐 **Navegadores:** Microsoft Edge, Waterfox, Firefox, Google Chrome e Brave.
  - 📦 **Gerenciadores de Pacotes (Multi-Distro):**
    - **Ubuntu / Debian / Mint:** Limpa cache do `apt` (`apt-get clean` / `autoremove`).
    - **Arch / CachyOS / Manjaro:** Limpa pacotes do `pacman` e `yay` mantendo rollback seguro.
    - **Fedora / RHEL:** Limpa cache do `dnf` (`dnf clean all`).
    - **openSUSE:** Limpa cache do `zypper`.
    - **Flatpak:** Desinstala runtimes órfãos.
  - 🐳 **Docker / Podman:** Limpa build caches e containers parados.
  - 📋 **Logs & Crash Dumps:** Reduz logs acumulados do `journalctl` e remove coredumps.

- **📁 Localizador de Arquivos Gigantes:**
  - Escaneia pastas chave (`Downloads`, `Videos`, `Documents`, `Desktop`) e lista os maiores arquivos do disco (> 500 MB) em uma tabela visual.

- **🚀 Diagnóstico Anti-Travamentos & Otimização:**
  - **GPU Híbrida / Dedicada:** Alerta se a dGPU NVIDIA estiver ativa consumindo energia à toa em repouso e permite alternar para modo Integrado via `supergfxctl`.
  - **Ananicy-CPP:** Verifica o status do gerenciador de prioridade de processos em tempo real (anti-stuttering para jogos e janelas ativas).
  - **NVMe TRIM:** Checagem de manutenção preventiva de velocidade do SSD.

- **🌐 Suporte Multilíngue (i18n):**
  - Alterne entre Português (pt-BR) e Inglês (en-US) na instalação, via flag (`--lang pt|en`) ou direto no menu interativo.

- **🛡 Segurança Primeiro:**
  - Se você digitar acidentalmente `cleanmyos` ou `clean` sem flags, ele **não altera nada** — apenas exibe o menu de ajuda.

---

## 📦 Instalação (Qualquer Linux)

O instalador detecta automaticamente a sua distribuição e o seu shell (**Fish**, **Zsh** ou **Bash**), configurando o PATH e salvando o idioma preferido:

### Opção 1: Via Script de Instalação (Recomendado)
```bash
git clone https://github.com/.../cleanmyos.git
cd cleanmyos
chmod +x install.sh
./install.sh
```
*Durante a instalação, você poderá escolher entre Português (pt-BR) e Inglês (en-US).*

Para instalar direto em português sem perguntar:
```bash
./install.sh --lang=pt
```

### Opção 2: Auto-instalação pelo Python
```bash
python3 cleanmyos --install
```

### Opção 3: Executar com uv (usando `pyproject.toml`)
Se você preferir usar [uv](https://docs.astral.sh/uv/getting-started/installation/), pode rodar ou instalar o projeto diretamente:

```bash
# Rodar sem instalar globalmente
uv run --with rich python cleanmyos -i

# Ou instalar como ferramenta a partir do projeto local
uv tool install .
cleanmyos -i
```

---

## 💻 Como Usar

### 1. Painel Interativo Completo (Estilo CleanMyMac)
```bash
cleanmyos -i
# ou
clean -i
```
Abre o menu interativo com painel colorido no terminal permitindo escolher individualmente o que limpar ou fazer a faxina completa de uma vez.

### 2. Apenas Ver o Diagnóstico (Sem limpar nada)
```bash
cleanmyos -s
```

### 3. Ver Maiores Arquivos do Disco (> 500 MB)
```bash
cleanmyos -l
```

### 4. Limpeza Automática Segura
```bash
cleanmyos -y
```

### 5. Trocar Idioma a Qualquer Momento
```bash
cleanmyos --lang pt   # Português
cleanmyos --lang en   # Inglês
```

### 6. Ajuda
```bash
cleanmyos -h
```

---

## 🛠 Requisitos
- Qualquer distribuição Linux (Ubuntu, Debian, Fedora, Arch, openSUSE, etc.)
- Python 3.9+
- Pacote Python `rich` (instalado automaticamente pelo `install.sh`)
- Opcional: [uv](https://docs.astral.sh/uv/getting-started/installation/) para executar/instalar via `pyproject.toml`

---

## 🧪 Executando testes

O projeto usa o `unittest` nativo do Python (nenhuma dependência extra é necessária para rodar a suíte atual).

```bash
python3 -m unittest discover -s tests -v
```

Se você quiser usar `pytest` (dependência opcional de desenvolvimento):

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest -v
```

---

## 🧭 Desinstalação
Para remover do sistema:
```bash
./uninstall.sh
```
