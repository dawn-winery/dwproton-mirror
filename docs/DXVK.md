### DXVK forks available in dwproton (credits to proton-cachyos!)

| Environment variable | Description |
|---|---|
| `PROTON_DXVK_LLASYNC` | When set to `1`, enables the alternative DXVK with default config (`lowlatency` + `gplasync`). **Should NOT be used with anti-cheat/multiplayer games.** |
| `PROTON_DXVK_LOWLATENCY` | When set to `1`, enables only the `low-latency` component (`DXVK_CONFIG="dxvk.enableAsync=False"`). Safe to use with anti-cheat/multiplayer games. |
| `PROTON_DXVK_GPLASYNC` | When set to `1`, enables only the `gplasync` component (`DXVK_CONFIG="dxvk.framePace=max-frame-latency"`). **Should NOT be used with anti-cheat/multiplayer games.** |

> When any of these options is used, DXVK compiler threads are set to `NUMBER_OF_CPUS - 2` (minimum 3) to improve interactivity during shader compilation.