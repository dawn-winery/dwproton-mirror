# Changelog

## [dwproton-11.0-9]
Release superseding 11.0-8 due to various hotfixes.
- Updated Proton and components to `cachyos-11.0-20260703-slr`
- Reset `winepulse.drv` as the default audio driver due to issues in ZZZ with the PipeWire driver.
  - `PROTON_USE_PIPEWIRE=1` can still manually enable the driver.
- Added custom protonfix for AK: Endfield to help with loading times due to heavy disk writes (see https://dawn.wine/dawn-winery/dwproton/pulls/36).

## [dwproton-11.0-0]

- Changelogs init
