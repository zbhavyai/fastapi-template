# FastAPI Template

![Build](https://img.shields.io/github/actions/workflow/status/zbhavyai/fastapi-template/build.yml?label=Build)
![Release](https://img.shields.io/github/actions/workflow/status/zbhavyai/fastapi-template/release.yml?label=Release)
![License](https://img.shields.io/github/license/zbhavyai/fastapi-template?label=License)

A **starter template** for building backend applications with [FastAPI](https://fastapi.tiangolo.com/), the high-performance Python web framework.

## :sparkles: Tech Stack and Features

-  :zap: [FastAPI](http://fastapi.tiangolo.com/), the high-performance Python web framework
-  :open_file_folder: Defined project structure with ready-to-use [`pyproject.toml`](pyproject.toml) and [pydantic settings](app/core/settings.py)
-  :pen: [VS Code](https://code.visualstudio.com/) settings included
-  :art: [Ruff](https://docs.astral.sh/ruff/) for consistent code formatting and linting
-  :page_facing_up: [.editorconfig](https://editorconfig.org/) for consistent coding styles across editors
-  :broom: A `pre-commit` hook for style enforcement
-  :test_tube: [pytest](https://docs.pytest.org/en/stable/) tests to keep code honest
-  :whale: Containerization with Dockerfile and docker compose
-  :otter: Automatic [Podman](https://podman.io/)/[Docker](https://www.docker.com/) detection for local dev
-  :hammer_and_wrench: [Makefile](https://www.gnu.org/software/make/) targets for format, build, run, and container tasks
-  :vertical_traffic_light: [GitHub Actions](https://github.com/features/actions) for CI/CD
-  :label: Artifact versioning based on Git SHA or tag, both in CI/CD and local builds

## :rocket: Getting started

-  Before you start development on this project, run the prep target. This will install a hook that would check your commit for code formatting and lint issues.

   ```shell
   make prep
   ```

-  Run the application in dev mode that enables live coding.

   ```shell
   make dev
   ```

-  To format the code while developing, you may use for IDE and turn on the auto-formatting on save. You may also use the format target.

   ```shell
   make format
   ```

## :package: Packaging and running

1. Build the application

   ```shell
   make build

   # OR

   make container-build
   ```

1. Run the application

   ```shell
   make run

   # OR

   make container-run
   ```

## :page_facing_up: License

The FastAPI Template is licensed under the terms of the [MIT license](LICENSE).
