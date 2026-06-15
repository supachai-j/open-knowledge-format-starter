# Install

The OKF starter is a **pure-Python tool (no mandatory dependencies)** that works fully offline / air-gapped.
Requirements:

- **Python 3.13+** (every tool uses the stdlib only)
- **Git** (for version-controlling your bundle)
- *(Optional)* **Ollama** if you want local semantic search
- *(Optional)* **Docker** if you want to self-host the server (Part 6)

## Option 1 — Install as a Claude Code skill (recommended)

This approach lets every project and every session create and maintain an OKF bundle without needing to be
inside the source repository.

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter

./install.sh                 # install globally → ~/.claude/skills/okf  (available to all projects)
./install.sh --project       # install for this project only → ./.claude/skills/okf
./install.sh --dir <path>    # install to a custom path
./install.sh --uninstall     # remove the installation
```

`install.sh` bundles the skill (the `SKILL.md` file + all Python tools + the embedded viewer library)
into a self-contained skill folder. Afterwards, open Claude Code and type `/okf` or say
*"init an OKF knowledge base here"* to get started.

> **How the skill works:** When invoked, Claude Code locates the skill and runs the scripts in its `scripts/`
> directory — regardless of whether it was installed globally or per-project.

## Option 2 — Use the repo directly

If you prefer to work inside the repository itself (or are not ready to install the skill yet), all tools
are available under `tools/`:

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter
python3 tools/okf-validate.py ./wiki        # → ✓ CONFORMANT with OKF v0.1
python3 tools/okf-viz.py ./wiki             # → wiki/viz.html (open in browser)
```

## Option 3 — Use as a GitHub template

The source repository is configured as a **template repository** — click **"Use this template"** on GitHub
to create your own new repo with the full structure already in place.

## Verify the installation

```bash
python3 --version                  # should be 3.13 or higher
python3 tools/okf-validate.py --help 2>/dev/null || python3 tools/okf-validate.py ./wiki
```

If you see `✓ CONFORMANT with OKF v0.1`, you are ready to go. Let's create your first knowledge base →
[Create your first knowledge base](./first-kb.md)
