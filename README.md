# NovaBox — Windows Compatibility for Android

NovaBox is a standalone Android Windows-compatibility app. It is independent of GameVault and GameVault Cloud. The app is based on the pinned Winlator Android engine, with original NovaBox branding, a Vietnamese-first Driver Hub, local Windows containers, Steam library scanning, touch controls and gamepad profiles.

## Features

- Wine + Box64/Box86 Windows containers, including real local .exe execution through the upstream XServer/Wine runtime.
- Per-container Windows settings, desktop resolution, shortcuts, file manager and touch/gamepad controls.
- Driver Hub with GPU detection and upstream component installation for Box64, Turnip, DXVK, VKD3D and WineD3D.
- Existing upstream graphics backends: Turnip, Vortek, Zink, VirGL and Gladio.
- Steam Library page scans libraryfolders.vdf and appmanifest_*.acf inside a selected Windows container; launches installed AppIDs via that container's Steam client. Steam credentials and Steam Guard remain inside Steam.
- Original NovaBox adaptive vector icon and native Canvas splash screen, built during bootstrap without external bitmap downloads.

## Driver compatibility

There is no universal graphics driver for every Android GPU. Turnip is for compatible Adreno devices; do not install it as a Mali driver. Mali/Immortalis/Xclipse devices should keep their manufacturer driver available and only test backends supported by that device/engine version. Proprietary vendor drivers are not redistributed.

- DXVK: Direct3D 9/10/11 → Vulkan.
- VKD3D: Direct3D 12 → Vulkan.
- WineD3D: OpenGL-based fallback.
- D7VK/CNC DDraw: legacy DirectDraw games.

## Build the APK

The compact repo contains the NovaBox overlay and CI scripts. The full Winlator engine is fetched at a pinned commit and its Git submodules are initialized during the build.

Linux/macOS:

```bash
./scripts/bootstrap.sh
./scripts/build-local.sh
```

The GitHub Actions workflow .github/workflows/android.yml builds a debug APK on every push to main and on manual dispatch. The artifact is named NovaBox-Android-debug-apk. It is not a signed Play Store release.

The build requires JDK 17, Android SDK, Android NDK 24.0.8215888 and CMake 3.22.1. The workflow installs these versions. The APK output path is dist/NovaBox-debug.apk.

## Quick start

1. Create a separate Windows environment for each game or app.
2. Import or download a Windows installer you are authorized to use, then launch the .exe from the container.
3. Start with automatic graphics selection and a conservative resolution such as 960×540.
4. Use DXVK only when Vulkan is functional; use VKD3D only for D3D12 apps whose GPU supports the required Vulkan features. Keep WineD3D as fallback.
5. In Steam Library, install Steam inside the container, sign in inside Steam, then scan installed libraries.

Not every Windows title will run on Android. Performance depends on CPU ISA, RAM, GPU, graphics drivers, game engine and thermal limits. The first start installs system files and uses substantial storage.

## Upstream and license

The engine uses Winlator from https://github.com/brunodev85/winlator at commit 30aafbdb9eea47b92669201621e03cd2cf04540d. Winlator is LGPL-2.1. Its app, vortek and gladio submodules are fetched unchanged; preserve their copyright and license notices. See THIRD_PARTY_NOTICES.md.

NovaBox is unofficial and is not affiliated with Winlator, Wine, Mesa, Qualcomm, ARM, Samsung, Microsoft, Steam or any game publisher.

## Local checks

```bash
python3 tests/test_files.py
bash -n scripts/bootstrap.sh scripts/build-local.sh
python3 -m py_compile scripts/apply_branding.py scripts/layout_overlay.py
```

These checks validate the overlay and automation; only the Android SDK/NDK build and device testing validate the APK/runtime.
