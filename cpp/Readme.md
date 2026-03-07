# C++ CMake Release Pipeline (GitHub Actions)

A generic CI/CD workflow for any C++ project using CMake. Builds on Windows, Linux (GCC + Clang), and macOS on every PR, then packages and publishes a GitHub Release on version tags.

---

## What it does

**On every pull request** — builds your project across all 4 platforms to catch compiler-specific issues early.

**On a version tag push (e.g. `v1.2.0`)** — additionally:
1. Packages the Windows build into a `.zip` (exe + DLLs)
2. Packages the macOS build into a `.app` bundle (with `Info.plist`) zipped up
3. Creates a GitHub Release with both zips attached
4. Auto-marks the release as a pre-release if the tag contains `alpha`, `beta`, or `rc`

---

## Setup

### 1. Replace all placeholders

Search the file for `<PLACEHOLDER` and fill in each one:

| Placeholder | What to put |
|---|---|
| `<PLACEHOLDER_PROJECT_NAME>` | Your project name, e.g. `MyApp` |
| `<PLACEHOLDER_EXE_NAME>` | The name of the compiled binary CMake produces, e.g. `MyApp` |
| `<PLACEHOLDER: apt packages ...>` | Linux system dependencies, e.g. `libsdl2-dev libglfw3-dev` — delete the step entirely if you have none |
| `<PLACEHOLDER: reverse-domain id>` | macOS bundle ID, e.g. `com.yourname.myapp` |
| `<PLACEHOLDER: add any usage instructions>` | Release notes body — what users should know |

### 2. Make sure your CMakeLists.txt names the binary correctly

The workflow looks for a binary named `<PLACEHOLDER_EXE_NAME>`. Make sure your `CMakeLists.txt` uses the same name:

```cmake
add_executable(<PLACEHOLDER_EXE_NAME> src/main.cpp ...)
```

### 3. Copy the workflow into your repo

```
your-repo/
└── .github/
    └── workflows/
        └── ci.yml   ← paste the workflow here
```

### 4. Push a tag to trigger a release

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## Assets / Resources

If your project has an `assets/` folder (textures, sounds, configs, etc.), uncomment these lines in both the Windows and macOS packaging steps:

```yaml
# Copy assets/resources if your project has them
# cp -r assets release/<PLACEHOLDER_PROJECT_NAME>/
```

---

## Adding itch.io deploys

If you want to deploy to itch.io after the GitHub Release, add a `deploy-itch` job. You'll need:

- A `BUTLER_API_KEY` secret in your repo (from https://itch.io/user/settings/api-keys)
- Your itch.io username and project slug

```yaml
deploy-itch:
  name: Deploy to itch.io
  needs: [build, release]
  runs-on: ubuntu-latest
  if: startsWith(github.ref, 'refs/tags/')

  steps:
    - uses: actions/download-artifact@v4
      with:
        name: windows-release

    - uses: actions/download-artifact@v4
      with:
        name: macos-release

    - name: Install Butler
      run: |
        curl -L -o butler.zip https://github.com/itchio/butler/releases/latest/download/butler-linux-amd64.zip
        unzip butler.zip
        chmod +x linux-amd64/butler
        echo "$PWD/linux-amd64" >> $GITHUB_PATH

    - name: Push Windows to itch.io
      env:
        BUTLER_API_KEY: ${{ secrets.BUTLER_API_KEY }}
      run: |
        butler push \
          "<PLACEHOLDER_PROJECT_NAME>-${{ github.ref_name }}-windows.zip" \
          <PLACEHOLDER: itchio-username/project-slug>:windows \
          --userversion "${{ github.ref_name }}"

    - name: Push macOS to itch.io
      env:
        BUTLER_API_KEY: ${{ secrets.BUTLER_API_KEY }}
      run: |
        butler push \
          "<PLACEHOLDER_PROJECT_NAME>-${{ github.ref_name }}-macos.zip" \
          <PLACEHOLDER: itchio-username/project-slug>:osx \
          --userversion "${{ github.ref_name }}"
```

---

## Platform matrix

The workflow builds on all 4 targets by default. To remove a platform, delete its entry from the `matrix.platform` list:

```yaml
matrix:
  platform:
    - { name: Windows MSVC, os: windows-latest, flags: "" }
    - { name: Linux GCC,    os: ubuntu-latest,  flags: "" }
    - { name: Linux Clang,  os: ubuntu-latest,  flags: -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ }
    - { name: macOS,        os: macos-latest,   flags: "" }
```

Note that only Windows and macOS are packaged and released — Linux builds are CI-only (compile + verify).