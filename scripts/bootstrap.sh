#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/winlator"
PIN="30aafbdb9eea47b92669201621e03cd2cf04540d"

mkdir -p "$ROOT/vendor"
if [ ! -d "$VENDOR/.git" ]; then
  git clone https://github.com/brunodev85/winlator.git "$VENDOR"
fi

git -C "$VENDOR" fetch --depth 1 origin "$PIN"
git -C "$VENDOR" checkout --detach "$PIN"
git -C "$VENDOR" submodule sync --recursive
git -C "$VENDOR" submodule update --init --recursive

python3 "$ROOT/scripts/apply_branding.py" "$VENDOR"
echo "NovaBox source prepared at: $VENDOR"
