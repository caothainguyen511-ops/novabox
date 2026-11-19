# NovaBox driver compatibility matrix

| GPU | Initial Vulkan path | Initial OpenGL path | Notes |
|---|---|---|---|
| Qualcomm Adreno | Turnip, if compatible | Gladio or system | Keep the vendor driver available as fallback. |
| ARM Mali / Immortalis | Vortek where supported; system Vulkan otherwise | Gladio / system | Never install Turnip as a Mali driver. |
| Samsung Xclipse | System Vulkan or Vortek where tested | System / Gladio | Compatibility varies by SoC and Android build. |
| Unknown | Automatic upstream choice | Automatic upstream choice | Start conservatively and test a single change at a time. |

NovaBox uses component manifests and download indexes from the pinned upstream Winlator component manager. It does not bundle proprietary Qualcomm, ARM or Samsung driver binaries. A driver package must match the device, Android release, architecture and license.

## Direct3D translation layers

- DXVK: Direct3D 9, 10 and 11 over Vulkan.
- VKD3D: Direct3D 12 over Vulkan; separate from DXVK.
- WineD3D: OpenGL fallback for applications that do not work with Vulkan.
- D7VK / CNC DDraw: selected legacy DirectDraw software.

Do not force the newest component onto every GPU. Use the versions selected by the upstream engine and keep a known-good container profile.
