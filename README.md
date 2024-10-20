

pre-commit-hooks
================

[![CI Build](https://github.com/rcolfin/pre-commit-hooks/actions/workflows/ci.yml/badge.svg)](https://github.com/rcolfin/pre-commit-hooks/actions/workflows/ci.yml)

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/rcolfin/pre-commit-hooks
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
      - id: mypy-linter
      - id: shellcheck-linter
```

#### mypy-linter

This expects poetry to be used.

To check the pre-commit:

```sh
pre-commit run --all-files --verbose
```
