#!/usr/bin/env bash

set -euo pipefail

REPO_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )
SCRIPTS_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$REPO_PATH"

exec "${SCRIPTS_PATH}/tag.sh" "$(git tag)"
