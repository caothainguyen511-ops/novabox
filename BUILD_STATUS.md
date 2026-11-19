# NovaBox project status

## Latest successful Android build

- GitHub Actions run: https://github.com/caothainguyen511-ops/novabox/actions/runs/44432745420
- Build commit: 011fb9c62888089ab73b85a6b8392e7c11c4a2cd
- Result: SUCCESS
- Workflow artifact: NovaBox-Android-debug-apk
- Artifact ID: 14487725505
- Artifact ZIP size: 156,672,050 bytes
- APK output: dist/NovaBox-debug.apk
- Downloaded APK SHA-256: c691445903985b91511cac8c7be14d418006e40be85ee5527f5a83fc472e8b1d
- APK size: 157,567,458 bytes
- Package artifact includes classes.dex and arm64-v8a native libraries for Winlator, Vortek, Gladio and VirGL.
- This is a debug APK, not a Play Store-signed release.

## Project structure
- Standalone repository: caothainguyen511-ops/novabox
- Independent of GameVault and GameVault Cloud.
- Engine: Winlator pinned to 30aafbdb9eea47b92669201621e03cd2cf04540d.
- Build workflow: .github/workflows/android.yml.
- Runtime: Wine + Box64/Box86, upstream XServer, container manager and Direct3D wrappers.

## NovaBox additions
- Original purple/cyan adaptive launcher icon and native Canvas splash.
- Vietnamese-first menu and dark NovaBox theme.
- Driver Hub, GPU detection and component installer controls.
- Steam Library scanner for local libraryfolders.vdf and appmanifest_*.acf with -applaunch support.
- Existing controller, touch controls, container and shortcut functionality retained.

## Verified checks
- Offline overlay fixture tests passed, including two successive patch applications.
- Bash script syntax checks passed.
- Python patcher compilation checks passed.
- Upstream pinned engine and all declared submodules bootstrapped successfully.
- Gradle/CMake debug APK build completed successfully in GitHub Actions.
- APK archive integrity verified after download.
- Device installation and game-by-game runtime testing have not yet been performed.

## Limitations
- No universal Mali or Adreno vendor driver can safely be bundled for every phone.
- Steam titles must already be installed in the selected Windows container.
- Not every desktop Windows game is compatible with Android ARM hardware.
- Performance depends on GPU/Vulkan support, RAM, thermals and the game.
