# CI/CD Pipeline Templates

A collection of ready-to-use GitHub Actions CI/CD workflows for common languages and stacks. Each template includes lint, test, Docker build, and push to Docker Hub.

## Structure

```
ci-cd-pipeline-template/
├── python/       # Flask app — flake8 + unittest
├── nodejs/       # Express app — eslint + jest
├── java/         # Maven app — checkstyle + JUnit
├── go/           # HTTP server — golangci-lint + go test
├── cpp/          # CMake project — clang-tidy + ctest
└── csharp/       # ASP.NET app — dotnet format + xunit
```

## How Each Pipeline Works

Every workflow follows the same three-stage pattern:

```
lint → test → build & push (main branch only)
```

1. **Lint** — catches style and formatting issues early
2. **Test** — runs the test suite; blocks the push stage if tests fail
3. **Build & Push** — builds the Docker image and pushes to Docker Hub (only on merges to `main`, not on PRs)

## Setup

### 1. Add Docker Hub secrets to your GitHub repo

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | A Docker Hub access token (not your password) |

> Generate a token at: https://hub.docker.com/settings/security

### 2. Update the image name

In each workflow file, replace:
```yaml
env:
  IMAGE_NAME: your-dockerhub-username/your-app-name
```

### 3. Copy the template into your project

Copy the relevant folder's contents into your repo. The `.github/workflows/ci-cd.yml` file is what GitHub Actions picks up automatically.

## Templates

| Language | Runtime | Linter | Test Framework | 
|---|---|---|---|
| Python | 3.13 | flake8 | unittest |
| Node.js | 20 | eslint | jest |
| Java | 21 (Temurin) | Checkstyle | JUnit (via Maven) |
| Go | 1.22 | golangci-lint | go test |
| C++ | GCC 13 | clang-tidy | ctest |
| C# | .NET 8 | dotnet format | xunit |

## Docker Images

All Dockerfiles use a **multi-stage build** pattern (where applicable) to keep final image sizes small — a build stage compiles/installs, and a slim runtime stage runs the app.

Images are tagged with both `:latest` and the commit SHA (`:abc1234`) for traceability.