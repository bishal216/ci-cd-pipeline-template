# Python Desktop App — Windows Release Pipeline

Builds a Python app into a standalone Windows `.exe` using PyInstaller, packages it with assets into a ZIP, and publishes it as a GitHub Release on every push to `main`.

Users don't need Python installed — the executable is fully self-contained.

---

## Setup

### 1. Replace all placeholders

| Placeholder | What to put |
|---|---|
| `<PLACEHOLDER_ENTRY_POINT>` | Your script's filename without `.py`, e.g. `game` or `main` |
| `<PLACEHOLDER_PROJECT_NAME>` | Your project name used in the ZIP filename, e.g. `my-app` |
| `<PLACEHOLDER: your app's dependencies>` | Packages to `pip install`, e.g. `pygame matplotlib numpy` |

### 2. Add or remove asset folders

The workflow copies `assets/` and `data/` into the release ZIP by default. Add or remove `xcopy` lines to match your project structure:

```yaml
# Copy additional folders
xcopy /E /I /Y assets release\assets\
xcopy /E /I /Y data release\data\
xcopy /E /I /Y sounds release\sounds\
```

Also add a matching `--add-data` flag to the PyInstaller step for each folder:

```yaml
--add-data "sounds;sounds"
```

### 3. No secrets needed

The workflow uses the built-in `GITHUB_TOKEN` — no setup required.

---

## How releases work

Every push to `main` overwrites a single `latest` pre-release tag. This means there's always a fresh build available at a stable URL without needing to manage version tags.

To switch to versioned releases instead, trigger on tags:

```yaml
on:
  push:
    tags: [ 'v*' ]
```

And update the release step:

```yaml
- uses: softprops/action-gh-release@v2
  with:
    tag_name: ${{ github.ref_name }}
    name: "${{ github.ref_name }}"
    prerelease: false
```

---

## Useful PyInstaller flags

Add these to the `pyinstaller` command in the workflow as needed:

| Flag | Effect |
|---|---|
| `--windowed` | Hides the console window (for GUI apps) |
| `--icon=assets/icon.ico` | Sets a custom icon for the `.exe` |
| `--name MyApp` | Renames the output executable |
| `--onedir` | Produces a folder instead of a single file (faster startup) |

---

## Adding a Linux or macOS build

To also release for other platforms, add parallel jobs using the same pattern:

```yaml
build-linux:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"
    - run: pip install pyinstaller <your-deps>
    - run: pyinstaller --noconfirm --onefile <PLACEHOLDER_ENTRY_POINT>.py
    - run: |
        mkdir release && cp dist/<PLACEHOLDER_ENTRY_POINT> release/
        cp -r assets release/assets
        zip -r <PLACEHOLDER_PROJECT_NAME>-linux.zip release/
    - uses: softprops/action-gh-release@v2
      with:
        tag_name: latest
        files: <PLACEHOLDER_PROJECT_NAME>-linux.zip
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```