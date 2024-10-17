#!/usr/bin/env bash

REPO_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )

function log() {
    >&2 echo "$(date '+%Y-%m-%d %H:%M:%S') ${*}"
}

function fail() {
    log "${*}"
    exit 1
}

[ $# -le 0 ] && { fail "Tag missing."; }

cd "${REPO_PATH}" || { fail "Failed to change directory."; }

git fetch
git push origin --delete "$1"
git tag --delete "$1"
git tag "$1"
git push origin "$1" --tags
