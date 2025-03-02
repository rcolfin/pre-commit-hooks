# pre-commit-hooks

[![CI Build](https://github.com/rcolfin/pre-commit-hooks/actions/workflows/ci.yml/badge.svg)](https://github.com/rcolfin/pre-commit-hooks/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/rcolfin/pre-commit-hooks.svg)](https://github.com/rcolfin/pre-commit-hooks/blob/main/LICENSE)

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/rcolfin/pre-commit-hooks
    rev: v0.2.0
    hooks:
      - id: mypy-linter
      - id: shellcheck-linter
      - id: uv-check
      - id: uv-lock
```

#### mypy-linter

This expects  [poetry](https://python-poetry.org/) or [uv](https://docs.astral.sh/uv/) to be used.

To check the pre-commit hooks on all files:

```sh
pre-commit run --all-files --verbose
```

To check on the pre-commit hooks on select files:

```sh
pre-commit run --files ./pyproject.toml --verbose
```
