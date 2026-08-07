# Changelog

## [dwproton-11.0-11]
- Implemented missing features and fixed blockers preventing hololive Dreams from launching. Game now works out of the box!

## [dwproton-11.0-10]
- Added signature workaround for HSR. Game now works out of the box!
  - This is the same method we were using in our launchers for 3 years, and technically a less proper solution than [signed](https://github.com/dawn-winery/dawn-signed), but unlike locking the build to our signing key, it allows for community effort in dwproton development.
- Fixed Netmarble Launcher updates not working (https://dawn.wine/dawn-winery/dwproton/issues/39)
- Imported patch from Proton-EM fixing window decorations with CEF launchers (such as HoYoPlay)
- Fixed NIKKE protonfix auto-applying on Steam

## [dwproton-11.0-9]
Release superseding 11.0-8 due to various hotfixes.
- Updated Proton and components to `cachyos-11.0-20260703-slr`
- Reset `winepulse.drv` as the default audio driver due to issues in ZZZ with the PipeWire driver.
  - `PROTON_USE_PIPEWIRE=1` can still manually enable the driver.
- Added custom protonfix for AK: Endfield to help with loading times due to heavy disk writes (see https://dawn.wine/dawn-winery/dwproton/pulls/36).

## [dwproton-11.0-0]

- Changelogs init
