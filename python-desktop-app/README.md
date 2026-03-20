# Python Desktop App — CI/CD Pipeline

A plug-and-play GitHub Actions pipeline for Python desktop applications.
Lints, tests, builds, and releases a standalone Windows `.exe` inside a ZIP on every push to `main`.

---

## How the Pipeline Works

Every push to `main` triggers four jobs in order:

```
format → lint → test → build-and-release
```

| Job | Tool | Failure mode |
|-----|------|-------------|
| **Format** | `black --check` | Hard — blocks everything downstream |
| **Lint** | `flake8` | Hard — blocks build |
| **Lint** | `pylint` | Soft — warns but doesn't block |
| **Test** | `pytest --cov` | Hard — blocks build if coverage too low |
| **Build** | `pyinstaller` | Hard |
| **Release** | GitHub Release + ZIP | Hard |

> CI never modifies your code. If format or lint fails, fix it locally and push again.

---

## Project Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── build.yml       # CI/CD pipeline
├── tests/
│   └── test_*.py           # pytest tests
├── main.py                 # entry point (UI)
├── calculator.py           # app logic (imported by tests)
├── main.spec               # PyInstaller build config
├── setup.cfg               # flake8 + pylint + pytest config
├── requirements.txt        # pip dependencies
├── conftest.py             # makes root modules importable in tests
└── .gitignore
```

---

## Adapting This to Your Own Project

### 1. Update the env vars in `build.yml`

```yaml
env:
  PYTHON_VERSION: "3.14"      # Python version to use
  SPEC_FILE: "main.spec"      # your .spec filename
  OUTPUT_NAME: "main"         # must match name= in your .spec
  ZIP_NAME: "app-win.zip"     # output ZIP filename
  MIN_COVERAGE: "50"          # minimum test coverage %
  PYLINT_THRESHOLD: "7.0"     # minimum pylint score out of 10
```

### 2. Update `main.spec`

Change the entry point and output name:

```python
a = Analysis(
    ['your_app.py'],    #  your entry point
    ...
)

exe = EXE(
    ...
    name='your_app',    #  must match OUTPUT_NAME in build.yml
    console=False,      #  False for GUI, True for CLI
)
```

If your app needs asset folders (images, data files, etc.), uncomment and update `datas`:

```python
datas=[
    ('assets', 'assets'),
    ('data',   'data'),
],
```

Then mirror each folder in the "Package into ZIP" step in `build.yml`:

```yaml
xcopy /E /I /Y assets release\assets\
xcopy /E /I /Y data   release\data\
```

### 3. Update `setup.cfg`

```ini
[flake8]
max-line-length = 120
extend-ignore =
    E221

[pylint.MASTER]
ignore = venv, build, dist

[pylint.FORMAT]
max-line-length = 120

[tool:pytest]
testpaths = tests
```

Adjust `max-line-length` and `extend-ignore` to match your preferences.

### 4. Add your dependencies to `requirements.txt`

```
pygame==2.6.0
numpy==2.0.0
```

Leave it empty (or with a comment) if your app has no external dependencies.

### 5. Write tests in `tests/`

Keep your app logic separate from your UI so tests never need a display:

```
main.py          ← UI only  (imports from logic.py)
logic.py         ← pure logic (no GUI imports)
tests/
  test_logic.py  ← imports logic.py directly
```

This pattern lets pytest run headlessly in CI without a display server.

---

## Running Locally

### Format

```bash
black .
```

Always run this before pushing. CI runs `black --check` and will fail if your code isn't formatted.

### Lint

```bash
flake8 .
pylint --recursive=y .
```

Flake8 settings come from `setup.cfg` — don't pass flags on the command line.

### Test

```bash
pytest --cov=. --cov-report=term-missing
```

### Build (Windows only)

```bash
pip install pyinstaller
pyinstaller main.spec
```

Output is in `dist/`.

---

## Accessing Bundled Assets at Runtime

When PyInstaller bundles your app, the working directory changes.
Use this helper to locate files correctly both in dev and when frozen:

```python
import sys, os

def resource_path(relative: str) -> str:
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

# Usage:
img = pygame.image.load(resource_path('assets/player.png'))
```

---

## VS Code Setup

Install these extensions:
- `ms-python.black-formatter` — auto-format on save
- `ms-python.flake8` — inline lint warnings

Add to `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "black-formatter.args": ["--line-length", "120"]
}
```