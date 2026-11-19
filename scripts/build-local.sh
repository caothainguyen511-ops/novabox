#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/winlator"

"$ROOT/scripts/bootstrap.sh"
cd "$VENDOR/app"
chmod +x ./gradlew
./gradlew --no-daemon :app:assembleDebug

APK="$VENDOR/app/app/build/outputs/apk/debug/app-debug.apk"
if [ ! -f "$APK" ]; then
  echo "Build finished but APK was not found at $APK" >&2
  exit 1
fi

mkdir -p "$ROOT/dist"
cp "$APK" "$ROOT/dist/NovaBox-debug.apk"
echo "APK: $ROOT/dist/NovaBox-debug.apk"
