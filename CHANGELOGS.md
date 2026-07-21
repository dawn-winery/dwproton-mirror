# Changelog

## [dwproton-11.0-8]
- Imported Wine/Proton changes from latest bleeding edge.
- Updated DXVK/DXVK-NVAPI to latest master.
- Reset `winepulse.drv` as the default audio driver due to issues in ZZZ with `winepipewire.drv`.
  - winepipewire can still be enabled with `PROTON_USE_PIPEWIRE=1`.
- Added custom protonfix for AK: Endfield to help with loading times due to heavy disk writes (https://dawn.wine/dawn-winery/dwproton/pulls/36).

## [dwproton-11.0-0]

- Changelogs init
