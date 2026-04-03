# RapumaMD Roadmap

## Known Issues / Planned Work

### Right-click / desktop launcher support

Right-click invocation from a file manager (Nautilus, Thunar, etc.) currently has three blockers. These should be fixed together as a single pass.

#### 1. PATH is stripped in desktop launches

**Files:** `renderer.py`, `cli.py`

When launched from a file manager, the process inherits a minimal environment. `~/.local/bin` (where `pipx` installs `rapumamd`) and `/usr/local/bin` (common location for `pandoc`) are often absent. Both `pandoc` (called by name in `renderer.py`) and `xdg-open` (called by name in `cli.py`) will fail with `FileNotFoundError`.

**Fix:** At startup, resolve `pandoc` and `xdg-open` to absolute paths using `shutil.which()`. If either is not found, raise a clear error immediately rather than at subprocess call time.

#### 2. Errors are invisible with no terminal attached

**Files:** `cli.py`

All error output goes to `stderr` via `click.echo(..., err=True)`. With no terminal attached (right-click launch), errors disappear silently — the process just exits. The user gets no feedback.

**Fix:** In the `render` command's `except` block, detect whether stderr is a TTY (`sys.stderr.isatty()`). If not, fall back to a GUI error dialog. Options in order of preference:
- `subprocess.run(["zenity", "--error", "--text=..."])` — available on most GNOME desktops
- `subprocess.run(["notify-send", "RapumaMD Error", "..."])` — lighter, notification only
- Tkinter `messagebox.showerror(...)` — always available since Tkinter is already a dependency (used by the `settings` GUI)

Tkinter is the safest fallback since it's already a dependency.

#### 3. `xdg-open` failure is silently swallowed

**Files:** `cli.py`

`subprocess.Popen(["xdg-open", str(output)])` has no error handling. If `xdg-open` fails (not found, no viewer registered), the failure is ignored.

**Fix:** Use `subprocess.run` instead of `Popen` and check `returncode`. On failure, display a message (using the same GUI fallback from fix #2) telling the user the PDF was written successfully but could not be opened automatically, and show the output path.

---

### Minor / low priority

#### Duplicate `--from` flag passed to pandoc

**File:** `renderer.py:32,54`

Both `-f markdown` and `--from=markdown` are passed to pandoc in the same invocation. Pandoc ignores the duplicate silently. Remove the `-f markdown` at line 32 and keep only the `--from=markdown` at line 54 (which appears after the stdin marker `-`).
