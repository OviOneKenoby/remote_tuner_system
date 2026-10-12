# Dell artifact hashes

Actual extracted artifact bytes independently rehashed against every recorded entry. Full compact manifests, including compiler-ABI probe artifacts, are in [review result](DELL_REVIEW_RESULT.json). No artifact is published; no timestamp/path/binary normalization applied.

| Artifact | Build1 SHA-256 | Build2 SHA-256 | Build3 SHA-256 | Raw identity |
| --- | --- | --- | --- | --- |
| firmware.bin | `c3670b055bc964888f6ece334ee51db8bd734d47e03f093ed6c18ee6e75b21c8` | `04b90df112588d3fe5068bbd3a4e6fdc573b41ef877ce6a85b9412cbed5d4d56` | `f733f35e5fb247946d3a4693d4e074f87a4e1a5b68bd500c92e7e68786468b6f` | DIFFERENT |
| firmware.elf | `df5c59649d2301d6251cd21f3e0a8deebe34fe35888d73f33014f32fd068a799` | `e43143d9e00b7dfb65aa7f17f3371cf12e7c427279f57f24e94233f81bea0216` | `441b33168f9d131b86e1d47aa4f02b0958ab0a93cea1eeb1be1c257da2c81ea6` | DIFFERENT |
| 12_LVGL_Test.map | `a45322d52af2262284b38ab43ea6a452c9663063b22e5aa5e66264b8d0586f2a` | `c56fbca4d62c43cfb9e7a863eba7c049798293a90a2877643fa8dc5d7c31fdf7` | `e4f3046a2d594e8a8246226b86df3d9d6050bfef71df1a3b4a0f449a6de7acc8` | DIFFERENT |
| bootloader.bin | `2fb1e877703a2125e0e6b0901a0fdf97f0c9a27b3b686368fde9d723e9e9f8c0` | `770a00192bee87590c9b3ea25139c22469237ac156678edc1c9e90af929abdab` | `dfbefac376d51181d8e4b65cdcca9e35c9fceb9e872263e9021e9afda6e3f642` | DIFFERENT |
| bootloader.elf | `4248b328536b941fae230949da766d0335d33d2d411190d5e7caccfc8aa402b9` | `a2bb7e2220815c141b2cdb46bd576122d7d988d589ec673decd7a432f3800dcc` | `425656fd6db6e79f2eea2c4c77410a7adc5a0111cec456717807f5f58b08d59b` | DIFFERENT |
| partitions.bin | `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835` | `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835` | `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835` | IDENTICAL |
| ota_data_initial.bin | `7d2c7ac4888bfd75cd5f56e8d61f69595121183afc81556c876732fd3782c62f` | `7d2c7ac4888bfd75cd5f56e8d61f69595121183afc81556c876732fd3782c62f` | `7d2c7ac4888bfd75cd5f56e8d61f69595121183afc81556c876732fd3782c62f` | IDENTICAL |
| bootloader/bootloader.map | `38fb27e2b59b618defbec8432f21ac2a0ed384297e1286cdd03f4dd9d65f3731` | `38fb27e2b59b618defbec8432f21ac2a0ed384297e1286cdd03f4dd9d65f3731` | `38fb27e2b59b618defbec8432f21ac2a0ed384297e1286cdd03f4dd9d65f3731` | IDENTICAL |

Application sizes: build1/build2 2,485,824 bytes; build3 2,485,568 bytes. All application ELF files17,758,832 bytes; bootloader BIN20,832 bytes; partitions3,072 bytes. Historical A006 application SHA-256 `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`,2,485,824 bytes: DIFFERENT from every Dell application. Historical partition SHA matches all three Dell partitions exactly.
