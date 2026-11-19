# NovaBox project status

## Project structure
- This repository is a standalone Android project overlay, not part of GameVault.
- Engine: Winlator pinned to 30aafbdb9eea47b92669201621e03cd2cf04540d.
- Build workflow: .github/workflows/android.yml.
- Runtime: Wine + Box64/Box86, upstream XServer, container manager and Direct3D wrappers.

## NovaBox additions
- Original purple/cyan adaptive launcher icon and native Canvas splash.
- Vietnamese-first menu and dark NovaBox theme.
- Driver Hub, GPU detection and component installer controls.
- Steam Library scanner for local libraryfolders.vdf and appmanifest_*.acf with -applaunch support.
- Existing controller, touch controls, container and shortcut functionality retained.

## Current validation
- Offline overlay fixtures are tested with tests/test_files.py.
- Bash scripts are syntax-checked.
- Android SDK/NDK build runs in GitHub Actions and must complete before distributing an APK.
- A successful Gradle build does not replace device-level testing.

## Limitations
- No universal Mali or Adreno vendor driver can safely be bundled for every phone.
- Steam titles must already be installed in the selected Windows container.
- Not every desktop Windows game is compatible with Android ARM hardware.
