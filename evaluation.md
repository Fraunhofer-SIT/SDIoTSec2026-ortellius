# Evaluation

This document describes how the binaries in `input/` have been collected, and presents the experiment results.

## Collecting firmware binaries.
The directory `input/` contains a diverse set of firmware binaries to detect the target architecture of. They stem from two sources.

### `input/fuzzware_samples/`
This directory contains firmware binaries used in the evaluation of Fuzzware [1]. These binaries have been taken from the directory `examples/pw-recovery` in [the fuzzware repository on GitHub](https://github.com/fuzzware-fuzzer/fuzzware).

#### Fuzzware firmware details
The following firmware binaries have been taken from the Fuzzware repository:

1. `arch_pro.bin`
    * target architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * MCU represented in knowledge base: **yes** e.g. `LPC176x5x_v0.2.svd`
    * series represented in knowledge base: **yes**
2. `EFM32GG_STK3700.bin`
    * target architecture: `Silicon Labs EFM32GG990F1024`
        * series: `Silicon Labs EFM32GG`
    * MCU represented in knowledge base: **yes** e.g. `EFM32GG990F1024.svd`
    * series represented in knowledge base: **yes**
3. `EFM32LG_STK3600.bin`
    * target architecture: `Silicon Labs EFM32LG990F256`
        * series: `Silicon Labs EFM32LG`
    * MCU represented in knowledge base: **yes** e.g. `EFM32LG990F256.svd`
    * series represented in knowledge base: **yes**
4. `LPC1549.bin`
    * target architecture: `NXP LPC1549`
        * series: `NXP LPC15xx`
    * MCU represented in knowledge base: **yes** e.g. `LPC15xx_v0.7.svd`
    * series represented in knowledge base: **yes**
5. `LPC1768.bin`
    * target architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * MCU represented in knowledge base: **yes** e.g. `LPC176x5x_v0.2.svd`
    * series represented in knowledge base: **yes**
6. `MOTE_L152RC.bin`
    * target architecture: `STM32L152RC`
        * series: `STM32L1`
    * MCU represented in knowledge base: **yes** e.g. `STM32L152.svd`
    * series represented in knowledge base: **yes**
7. `NUCLEO_F103RB.bin`
    * target architecture: `STM32F103RB`
        * series: `STM32F1`
    * MCU represented in knowledge base: **yes** e.g. `STM32F103xx.svd`
    * series represented in knowledge base: **yes**
8. `NUCLEO_F207ZG.bin`
    * target architecture: `STM32F207ZG`
        * series: `STM32F2`
    * MCU represented in knowledge base: **yes** e.g. `STM32F20x.svd`
    * series represented in knowledge base: **yes**
9. `NUCLEO_L152RE.bin`
    * target architecture: `STM32L152RE`
        * series: `STM32L1`
    * MCU represented in knowledge base: **yes** e.g. `STM32L152.svd`
    * series represented in knowledge base: **yes**
10. `UBLOX_C027.bin`
    * target architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * MCU represented in knowledge base: **yes** e.g. `LPC176x5x_v0.2.svd`
    * series represented in knowledge base: **yes**

### `input/edgeimpulse/`
This directory contains binary images of Edge Impulse firmware intended to run on various embedded devices. Wherever possible, these images have been compiled from their respective Github repositories. For images, that we were unable to build ourselves, we downloaded pre-built images from [the Edge Impulse website](https://docs.edgeimpulse.com/hardware/). We did not compile or download firmware for devices, whose series is not represented in our knowledge base.

#### Edge Impulse firmware details

At the time of writing, there exist 37 Github repositories with URLs starting with `https://github.com/edgeimpulse/firmware-`. We will list details for the firmware provided by each repository here.

##### Not represented in knowledge base
The following firmware has not been compiled because its target architecture series are not represented in our knowledge base.

1. https://github.com/edgeimpulse/firmware-espressif-esp32
    * target architecture: `Espressif ESP32`
        * series: `Espressif ESP32`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
    * **note**: `cmsis-svd-data` *does* contain files for the ESP32, however none of them could be parsed with [svdsuite](https://pypi.org/project/svdsuite/).
2. https://github.com/edgeimpulse/firmware-eta-compute-ecm3532
    * target architecture: `Eta Compute ECM3532`
        * series: `Eta Compute ECM353x`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
3. https://github.com/edgeimpulse/firmware-himax-we-i-plus
    * target architecture: `Eta Compute ECM3532`
        * series: `Eta Compute ECM353x`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
4. https://github.com/edgeimpulse/firmware-nordic-nrf54l15dk
    * target architecture: `Nordic nRF54L15DK`
        * series: `Nordic nRF54`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
5. https://github.com/edgeimpulse/firmware-nordic-nrf7002dk
    * target architecture: `Nordic nRF7002DK`
        * series: `nRF70`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
6. https://github.com/edgeimpulse/firmware-particle
    * target architecture: `Realtek RTL8721DM`
        * series: `Realtek RTL872x`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
7. https://github.com/edgeimpulse/firmware-seeed-grove-vision-ai
    * target architecture: `Himax WE1`
        * series: `Himax WE1`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
8. https://github.com/edgeimpulse/firmware-sony-spresense
    * target architecture: `Sony CXD5602PWBMAIN1`
        * series: `Sony CXD56xx`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
9. https://github.com/edgeimpulse/firmware-synaptics-ka10000
    * target architecture: `Synaptics KA10000`
        * series: `Synaptics KA`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**
10. https://github.com/edgeimpulse/firmware-syntiant-tinyml
    * target architecture: `Syntiant NDP101`
        * series: `Syntiant NDP`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **no**

##### Successfully compiled firmware
The following firmware has been successfully compiled and is present in `input/edgeimpulse/`. Since multiple binaries may be compiled in one repository, we specify the path to each binary relative to the repository root.

1. https://github.com/edgeimpulse/firmware-ambiq-apollo5
    * target architecture: `Ambiq Apollo510`
        * series: `Ambiq Apollo5`
    * MCU represented in knowledge base: `apollo510.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/apollo510_evb/arm-none-eabi/firmware-ambiq-apollo5.bin`
    * name in this repo: `firmware-ambiq-apollo5.bin`
2. https://github.com/edgeimpulse/firmware-arduino-nano-33-ble-sense
    * target architecture: `Nordic nRF52840`
        * series: `Nordic nRF52`
    * MCU represented in knowledge base: `nrf52840.svd`
    * series represented in knowledge base: **yes**
    * binary path: `firmware-arduino-nano-33-ble-sense.ino.bin`
    * name in this repo: `firmware-arduino-nano-33-ble-sense.ino.bin`
3. https://github.com/edgeimpulse/firmware-arduino-nicla-vision
    * target architecture: `STM32H747`
        * series: `STM32H7`
    * MCU represented in knowledge base: **yes** e.g. `STM32H747_CM7.svd`
    * series represented in knowledge base: **yes**
    * binary path: `firmware-arduino-nicla-vision.ino.bin`
    * name in this repo: `firmware-arduino-nicla-vision.ino.bin`
4. https://github.com/edgeimpulse/firmware-arduino-nicla-voice
    * target architecture: `Nordic nRF52832`
        * series: `Nordic nRF52`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `nrf52833.svd`
    * binary path: `firmware-arduino-nicla-voice.ino.bin`
    * name in this repo: `firmware-arduino-nicla-voice.ino.bin`
5. https://github.com/edgeimpulse/firmware-arduino-portenta-h7
    * target architecture: `STM32H747XI`
        * series: `STM32H7`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `STM32H7.svd`
    * binary path: `firmware-arduino-portenta-h7.ino.bin`
    * name in this repo: `firmware-arduino-portenta-h7.ino.bin`
6. https://github.com/edgeimpulse/firmware-avnet-rasyn
    * target architecture: `Renesas RA6M4`
        * series: `Renesas RA6`
    * MCU represented in knowledge base: **yes** e.g. `R7FA6M4AF.svd`
    * series represented in knowledge base: **yes**
    * binary path: `Debug/firmware-avnet-rasyn.elf`
    * name in this repo: `firmware-avnet-rasyn.elf`
7. https://github.com/edgeimpulse/firmware-nordic-nrf52840dk-nrf5340dk (for target `Nordic nRF52840`)
    * target architecture: `Nordic nRF52840`
        * series: `Nordic nRF52`
    * MCU represented in knowledge base: `nrf52840.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/zephyr/zephyr.bin`
    * name in this repo: `firmware-nordic-nrf52840dk.bin`
    * **note**: We list this repository twice, as it contains firmware for two different target architectures.
8. https://github.com/edgeimpulse/firmware-nordic-nrf52840dk-nrf5340dk (for target `Nordic nRF5340`)
    * target architecture: `Nordic nRF5340`
        * series: `Nordic nRF53`
    * MCU represented in knowledge base: **yes** e.g. `nrf5340_application.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/zephyr/zephyr.bin`
    * name in this repo: `firmware-nordic-nrf5340dk.bin`
9. https://github.com/edgeimpulse/firmware-nordic-nrf9160dk
    * target architecture: `Nordic nRF9160`
        * series: `Nordic nRF91`
    * MCU represented in knowledge base: **yes** e.g. `nrf9160.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/zephyr/zephyr.bin`
    * name in this repo: `firmware-nordic-nrf9160dk.bin`
10. https://github.com/edgeimpulse/firmware-nordic-thingy53
    * target architecture: `Nordic nRF5340`
        * series: `Nordic nRF53`
    * MCU represented in knowledge base: **yes** e.g. `nrf5340_application.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/zephyr/app_update.bin`
    * name in this repo: `firmware-nordic-thingy53.bin`
11. https://github.com/edgeimpulse/firmware-nordic-thingy91
    * target architecture: `Nordic nRF9160`
        * series: `Nordic nRF91`
    * MCU represented in knowledge base: **yes** e.g. `nrf9160.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/zephyr/app_signed.hex`
    * name in this repo: `firmware-nordic-thingy91.hex`
12. https://github.com/edgeimpulse/firmware-pi-rp2xxx (for target `Raspberry Pi RP2040`)
    * target architecture: `Raspberry Pi RP2040`
        * series: `Raspberry Pi RP2`
    * MCU represented in knowledge base: **yes** e.g. `rp2040.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/ei_rp2040_firmware.elf`
    * name in this repo: `ei_rp2040_firmware.elf`
    * **note**: We list this repository thrice, as it contains firmware for three different target architectures.
13. https://github.com/edgeimpulse/firmware-pi-rp2xxx (for target `Raspberry Pi RP2350`)
    * target architecture: `Raspberry Pi RP2350`
        * series: `Raspberry Pi RP2`
    * MCU represented in knowledge base: **yes** e.g. `rp2350.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/ei_rp2350_firmware.elf`
    * name in this repo: `ei_rp2350_firmware.elf`
14. https://github.com/edgeimpulse/firmware-pi-rp2xxx (for target `Raspberry Pi RP2350 Wifi`)
    * target architecture: `Raspberry Pi RP2350`
        * series: `Raspberry Pi RP2`
    * MCU represented in knowledge base: **yes** e.g. `rp2350.svd`
    * series represented in knowledge base: **yes**
    * binary path: `build/ei_rp2350_firmware.elf`
    * name in this repo: `ei_rp2350_w_firmware.elf`
15. https://github.com/edgeimpulse/firmware-seeed-grove-vision-ai-module-v2
    * target architecture: `Himax WiseEye2`
        * series: `Himax WiseEye2`
    * MCU represented in knowledge base: **yes** e.g. `WE2_S.svd`
    * series represented in knowledge base: **yes**
    * binary path: `we2_image_gen_local/output_case1_sec_wlcsp/output.img`
    * name in this repo: `firmware-seeed-grove-vision-ai-module-v2.img`
16. https://github.com/edgeimpulse/firmware-ti-launchxl
    * target architecture: `TI CC1352P`
        * series: `TI CC13xx/CC26xx`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `CC13x0.svd`
    * binary path: `gcc/build/firmware-ti-launchxl.out`
    * name in this repo: `firmware-ti-launchxl.out`

##### Downloadeded pre-built firmware
We were unable to compile firmware for the following devices, and have instead downloaded pre-built images from the [Edge Impulse website](https://docs.edgeimpulse.com/hardware/).

1. https://github.com/edgeimpulse/firmware-alif-* (target: Alif E7 AI/ML Kit Gen2 HE core)
    * **note**: There appear to be two repositories (`firmware-alif-csolution` and `firmware-alif-e7`) containing firmware for the same target architecture. We were unable to build either, and used pre-built firmware from the Edge Impulse website.
    * target architecture: `Alif E7 AI/ML Kit Gen2 HE core`
        * series: `Alif E7`
    * MCU represented in knowledge base: **yes** e.g. `AE722F80F55D5LS_HE.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/alif-e7-gen2.zip
    * name in this repo: `firmware-alif-HE.bin`
    * **note**: We list this repository four times, as the website provides four firmware images for the Alif E7 series.
2. https://github.com/edgeimpulse/firmware-alif-* (target: Alif E7 AI/ML Kit Gen2 HP core)
    * target architecture: `Alif E7 AI/ML Kit Gen2 HP core`
        * series: `Alif E7`
    * MCU represented in knowledge base: **yes** e.g. `AE722F80F55D5AS_HP.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/alif-e7-gen2.zip
    * name in this repo: `firmware-alif-HP.bin`
3. https://github.com/edgeimpulse/firmware-alif-* (target: Alif E7 Dev Kit Gen2 HE core)
    * target architecture: `Alif E7 Dev Kit Gen2 HE core`
        * series: `Alif E7`
    * MCU represented in knowledge base: **yes** e.g. `AE722F80F55D5LS_HE.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/alif-e7-gen2.zip
    * name in this repo: `firmware-alif-HE_DEVKIT.bin`
4. https://github.com/edgeimpulse/firmware-alif-* (target: Alif E7 Dev Kit Gen2 HP core)
    * target architecture: `Alif E7 Dev Kit Gen2 HP core`
        * series: `Alif E7`
    * MCU represented in knowledge base: **yes** e.g. `AE722F80F55D5AS_HP.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/alif-e7-gen2.zip
    * name in this repo: `firmware-alif-HP_DEVKIT.bin`
5. https://github.com/edgeimpulse/firmware-ambiq-apollo4
    * target architecture: Ambiq Apollo4 Blue Plus EVB
        * series: `Ambiq Apollo4`
    * MCU represented in knowledge base: **yes** e.g. `apollo4b.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/build-system/ambiq-apollo4.zip
    * name in this repo: `firmware-ambiq-apollo4.bin`
6. https://github.com/edgeimpulse/firmware-brickml
    * target architecture: `Renesas RA6M5`
        * series: `Renesas RA6`
    * MCU represented in knowledge base: **yes** e.g. `R7FA6M5BH.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/brickml.zip
    * name in this repo: `firmware-brickml.bin.signed`
7. https://github.com/edgeimpulse/firmware-infineon-cy8ckit-062-ble
    * target architecture: `Infineon PSoC63`
        * series: `Infineon PSoC6`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `psoc63.svd`
    * downloaded from: https://cdn.edgeimpulse.com/firmware/infineon-cy8ckit-062-ble.zip
    * name in this repo: `firmware-infineon-cy8ckit-062-ble.hex`
8. https://github.com/edgeimpulse/firmware-infineon-cy8ckit-062s2
    * target architecture: `Infineon PSoC62S2`
        * series: `Infineon PSoC6`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `psoc63.svd`
    * downloaded from: https://cdn.edgeimpulse.com/firmware/infineon-cy8ckit-062s2.zip
    * name in this repo: `firmware-infineon-cy8ckit-062s2.hex`
9. https://github.com/edgeimpulse/firmware-nordic-nrf91x1 (target: Nordic nRF9151)
    * target architecture: `Nordic nRF9151`
        * series: `Nordic nRF91`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `nrf9160.svd`
    * downloaded from: https://cdn.edgeimpulse.com/firmware/nrf9151-dk.zip
    * name in this repo: `nrf9151-dk.hex`
    * **note**: We list this repository twice, as this repository provides firmware for two different target architectures.
10. https://github.com/edgeimpulse/firmware-nordic-nrf91x1 (target: Nordic nRF9161)
    * target architecture: `Nordic nRF9161`
        * series: `Nordic nRF91`
    * MCU represented in knowledge base: **no**
    * series represented in knowledge base: **yes** e.g. `nrf9160.svd`
    * downloaded from: https://cdn.edgeimpulse.com/firmware/nrf9161-dk.zip
    * name in this repo: `firmware-nrf9161-dk.hex`
11. https://github.com/edgeimpulse/firmware-renesas-ck-ra6m5
    * target architecture: `Renesas RA6M5`
        * series: `Renesas RA6`
    * MCU represented in knowledge base: **yes** e.g. `R7FA6M5BH.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/renesas-ck-ra6m5.zip
    * name in this repo: `firmware-renesas-ck-ra6m5.hex`
12. https://github.com/edgeimpulse/firmware-renesas-ek-ra8d1-freertos
    * target architecture: `Renesas RA8D1`
        * series: `Renesas RA8`
    * MCU represented in knowledge base: **yes** e.g. `R7FA8D1BH.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/renesas-ek-ra8d1.zip
    * name in this repo: `firmware-renesas-ek-ra8d1-freertos.hex`
13. https://github.com/edgeimpulse/firmware-silabs-thunderboard-sense-2
    * target architecture: `Silicon Labs EFR32MG12`
        * series: `Silicon Labs EFR32MG`
    * MCU represented in knowledge base: **yes** e.g. `EFR32MG12P231F1024GM68.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/silabs-thunderboard-sense2.bin
    * name in this repo: `silabs-thunderboard-sense-2.bin`
14. https://github.com/edgeimpulse/firmware-silabs-xg24
    * target architecture: `Silicon Labs EFR32xG24`
        * series: `Silicon Labs EFR32xG`
    * MCU represented in knowledge base: **yes** e.g. `EFR32MG24A420F1536IM40.json`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/silabs-xg24.zip
    * name in this repo: `firmware-xg24.hex`
15. https://github.com/edgeimpulse/firmware-st-b-l475e-iot01a
    * target architecture: `STM32L475VG`
        * series: `STM32L4`
    * MCU represented in knowledge base: **yes** e.g. `STM32L4x5.svd`
    * series represented in knowledge base: **yes**
    * downloaded from: https://cdn.edgeimpulse.com/firmware/DISCO-L475VG-IOT01A.bin
    * name in this repo: `DISCO-L475VG-IOT01A.bin`
16. https://github.com/edgeimpulse/firmware-st-stm32n6
    * target architecture: `STM32N6570`
        * series: `STM32N6`
    * MCU represented in knowledge base: **yes** e.g. `STM32N657.svd`
    * series represented in knowledge base: **yes**
    * pre-built binary copied from git repo: Upload/firmware-st-stm32n6.bin
    * name in this repo: `firmware-st-stm32n6.bin`

##### Could not obtain firmware
The following repositories could not be built, and we were unable to obtain pre-built firmware for them.

1. https://github.com/edgeimpulse/firmware-himax-ism
    * target architecture: `Himax WE2`
        * series: `Himax WE2`
    * MCU represented in knowledge base: **yes**, e.g. `WE2_S.svd`
    * series represented in knowledge base: **yes**


## Identification results

We only evaluated binaries for which the target architecture series is represented in our knowledge base. One binary could not be obtained and, thus, was not considered. In total, this amounts to 42 binaries (10 from the Fuzzware sample and 32 from Edge Impulse). The precise results for each binary are listed in `output/`. Below, we summarize the precision of the results.

We use the following scale to indicate whether the target architecture was correctly identified:
* **yes**: The exact target architecture was identified.
* **series only**: The target architecture series was correctly identified, but not the exact target.
* **no**: The target architecture was not correctly identified.
* *series not in database*: The target architecture series is not represented in the respective knowledge base

### Fuzzware sample results
* `arch_pro.bin`
    * actual target:
        * architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
* `EFM32GG_STK3700.bin`
    * actual target:
        * architecture: `Silicon Labs EFM32GG990F1024`
        * series: `Silicon Labs EFM32GG`
    * target identified:
        * cmsis-svd-data: **no** (detected: `EFM32ZG108`)
        * Keil: **no** (detected: `EFM32ZG108`)
        * combined: **no** (detected: `EFM32ZG108`)
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **no**
        * combined: **no**
* `EFM32LG_STK3600.bin`
    * actual target:
        * architecture: `Silicon Labs EFM32LG990F256`
        * series: `Silicon Labs EFM32LG`
    * target identified:
        * cmsis-svd-data: **no** (detected: `EFM32ZG108`)
        * Keil: **no** (detected: `EFM32ZG108`)
        * combined: **no** (detected: `EFM32ZG108`)
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **no**
        * combined: **no**
* `LPC1549.bin`
    * actual target:
        * architecture: `NXP LPC1549`
        * series: `NXP LPC15xx`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
* `LPC1768.bin`
    * actual target:
        * architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
* `MOTE_L152RC.bin`
    * actual target:
        * architecture: `STM32L152RC`
        * series: `STM32L1`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32L100`)
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `NUCLEO_F103RB.bin`
    * actual target:
        * architecture: `STM32F103RB`
        * series: `STM32F1`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32F102xx`)
        * Keil: **no** (detected: `PY32F001xx`)
        * combined: **no** (detected: `PY32F001xx`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **no**
        * combined: **no**
* `NUCLEO_F207ZG.bin`
    * actual target:
        * architecture: `STM32F207ZG`
        * series: `STM32F2`
    * target identified:
        * cmsis-svd-data: **no** (detected: `STM32F410`)
        * Keil: **no** (detected: `HT32F61030`)
        * combined: **no** (detected: `HT32F61030`)
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **no**
        * combined: **no**
* `NUCLEO_L152RE.bin`
    * actual target:
        * architecture: `STM32L152RE`
        * series: `STM32L1`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32L100`)
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `UBLOX_C027.bin`
    * actual target:
        * architecture: `NXP LPC1768`
        * series: `NXP LPC17xx`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**

### Edge Impulse results
* `firmware-ambiq-apollo5.bin`
    * actual target:
        * architecture: `Ambiq Apollo510`
        * series: `Ambiq Apollo5`
    * target identified:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
* `firmware-arduino-nano-33-ble-sense.ino.bin`
    * actual target:
        * architecture: `Nordic nRF52840`
        * series: `Nordic nRF52`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `nrf52820`)
        * Keil: **yes**
        * combined: **series only** (detected: `nrf52820`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `firmware-arduino-nicla-vision.ino.bin`
    * actual target:
        * architecture: `STM32H747`
        * series: `STM32H7`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32H750x`)
        * Keil: **series only** (detected: `STM32H723`)
        * combined: **series only** (detected: `STM32H750x`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-arduino-nicla-voice.ino.bin`
    * actual target:
        * architecture: `Nordic nRF52832`
        * series: `Nordic nRF52`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `nrf52805`) *only series in database*
        * Keil: **series only** (detected: `nrf52805`) *only series in database*
        * combined: **series only** (detected: `nrf52805`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-arduino-portenta-h7.ino.bin`
    * actual target:
        * architecture: `STM32H747XI`
        * series: `STM32H7`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32H74xx`) *only series in database*
        * Keil: **series only** (detected: `STM32H742x`)
        * combined: **series only** (detected: `STM32H74xx`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-avnet-rasyn.elf`
    * actual target:
        * architecture: `Renesas RA6M4`
        * series: `Renesas RA6`
    * target identified:
        * cmsis-svd-data: **no** (detected: `R7FA4E10D`)
        * Keil: **no** (detected: `R7FA4E10D`)
        * combined: **no** (detected: `R7FA4E10D`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-nordic-nrf52840dk.bin`
    * actual target:
        * architecture: `Nordic nRF52840`
        * series: `Nordic nRF52`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `nrf52810`)
        * Keil: **series only** (detected: `nrf52810`)
        * combined: **series only** (detected: `nrf52810`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `firmware-nordic-nrf5340dk.bin`
    * actual target:
        * architecture: `Nordic nRF5340`
        * series: `Nordic nRF53`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **no** (detected: `BAT32G137A`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **no**
* `firmware-nordic-nrf9160dk.bin`
    * actual target:
        * architecture: `Nordic nRF9160`
        * series: `Nordic nRF91`
    * target identified:
        * cmsis-svd-data: **no** (detected: `STM32F301`)
        * Keil: **no** (detected: `ATSAMG51`)
        * combined: **no** (detected: `ATSAMG51`)
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **no**
        * combined: **no**
* `firmware-nordic-thingy53.bin`
    * actual target:
        * architecture: `Nordic nRF5340`
        * series: `Nordic nRF53`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: *series not in database*
        * combined: **yes**
* `firmware-nordic-thingy91.hex`
    * actual target:
        * architecture: `Nordic nRF9160`
        * series: `Nordic nRF91`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `ei_rp2040_firmware.elf`
    * actual target:
        * architecture: `Raspberry Pi RP2040`
        * series: `Raspberry Pi RP2`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `ei_rp2350_firmware.elf`
    * actual target:
        * architecture: `Raspberry Pi RP2350`
        * series: `Raspberry Pi RP2`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: **series only** (detected: `RP2040`) *only series in database*
        * combined: **series only** (detected: `RP2040`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **series only**
        * combined: **yes**
* `ei_rp2350_w_firmware.elf`
    * actual target:
        * architecture: `Raspberry Pi RP2350 Wifi`
        * series: `Raspberry Pi RP2`
    * target identified:
        * cmsis-svd-data: **yes**
        * Keil: **series only** (detected: `RP2040`) *only series in database*
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **series only**
        * combined: **yes**
* `firmware-seeed-grove-vision-ai-module-v2.img`
    * actual target:
        * architecture: `Himax WiseEye2`
        * series: `Himax WiseEye2`
    * target identified:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
* `firmware-ti-launchxl.out`
    * actual target:
        * architecture: `TI CC1352P`
        * series: `TI CC13xx/CC26xx`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `CC13x0/CC26x0`) *only series in database*
        * Keil: *series not in database*
        * combined: **series only** (detected: `CC13x0/CC26x0`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: *series not in database*
        * combined: **series only**

* `firmware-alif-HE.bin`
    * actual target:
        * architecture: `Alif E7 AI/ML Kit Gen2 HE core`
        * series: `Alif E7`
    * target identified:
        * cmsis-svd-data: **no** (detected: `ATSAMS70J21`)
        * Keil: *series not in database*
        * combined: **no** (detected: `MCXW235`)
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: *series not in database*
        * combined: **no**
* `firmware-alif-HP.bin`
    * actual target:
        * architecture: `Alif E7 AI/ML Kit Gen2 HP core`
        * series: `Alif E7`
    * target identified:
        * cmsis-svd-data: **no** (detected: `ATSAMS70J21`) *only series in database*
        * Keil: *series not in database*
        * combined: **no** (detected: `PIC32CX2051MTG64`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: *series not in database*
        * combined: **no**
* `firmware-alif-HE_DEVKIT.bin`
    * actual target:
        * architecture: `Alif E7 Dev Kit Gen2 HE core`
        * series: `Alif E7`
    * target identified:
        * cmsis-svd-data: **no** (detected: `Alif E302`) *only series in database*
        * Keil: *series not in database*
        * combined: **no** (detected: `Himax WE2`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: *series not in database*
        * combined: **no**
* `firmware-alif-HP_DEVKIT.bin`
    * actual target:
        * architecture: `Alif E7 Dev Kit Gen2 HP core`
        * series: `Alif E7`
    * target identified:
        * cmsis-svd-data: **no** (detected: `Alif E302`) *only series in database*
        * Keil: *series not in database*
        * combined: **no** (detected: `Himax WE2`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: *series not in database*
        * combined: **no**
* `firmware-ambiq-apollo4.bin`
    * actual target:
        * architecture: `Ambiq Apollo4 Blue Plus EVB`
        * series: `Ambiq Apollo4`
    * target identified:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
* `firmware-brickml.bin.signed`
    * actual target:
        * architecture: `Renesas RA6M5`
        * series: `Renesas RA6`
    * target identified:
        * cmsis-svd-data: **no** (detected: `R7FA4E10D`)
        * Keil: **no** (detected: `R7FA4E10D`)
        * combined: **no** (detected: `R7FA4E10D`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **yes**
        * combined: **yes**
* `firmware-infineon-cy8ckit-062-ble.hex`
    * actual target:
        * architecture: `Infineon PSoC62`
        * series: `Infineon PSoC6`
    * target identified:
        * cmsis-svd-data: **series only** *only series in database*
        * Keil: **no** (detected: `Himax WE2`) *only series in database*
        * combined: **no** (detected: `Himax WE2`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-infineon-cy8ckit-062s2.hex`
    * actual target:
        * architecture: `Infineon PSoC62S2`
        * series: `Infineon PSoC6`
    * target identified:
        * cmsis-svd-data: **series only** *only series in database*
        * Keil: **no** (detected: `Himax WE2`) *only series in database*
        * combined: **no** (detected: `Himax WE2`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `nrf9151-dk.hex`
    * actual target:
        * architecture: `Nordic nRF9151`
        * series: `Nordic nRF91`
    * target identified:
        * cmsis-svd-data: **no** (detected: `STM32F410`) *only series in database*
        * Keil: **no** (detected: `Himax WE2`) *only series in database*
        * combined: **no** (detected: `Himax WE2`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **series only**
        * combined: **no**
* `nrf9161-dk.hex`
    * actual target:
        * architecture: `Nordic nRF9161`
        * series: `Nordic nRF91`
    * target identified:
        * cmsis-svd-data: **no** (detected: `STM32F410`) *only series in database*
        * Keil: **no** (detected: `Himax WE2`) *only series in database*
        * combined: **no** (detected: `Himax WE2`) *only series in database*
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **series only**
        * combined: **no**
* `firmware-renesas-ck-ra6m5.hex`
    * actual target:
        * architecture: `Renesas RA6M5`
        * series: `Renesas RA6`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `R7FA6E10F`)
        * Keil: **series only** (detected: `R7FA6E10F`)
        * combined: **series only** (detected: `R7FA6E10F`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **series only**
        * combined: **series only**
* `firmware-renesas-ek-ra8d1-freertos.hex`
    * actual target:
        * architecture: `Renesas RA8D1`
        * series: `Renesas RA8`
    * target identified:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**
* `silabs-thunderboard-sense-2.bin`
    * actual target:
        * architecture: `Silicon Labs EFR32MG12`
        * series: `Silicon Labs EFR32MG`
    * target identified:
        * cmsis-svd-data: **no** (detected: `EFR32FG1`)
        * Keil: **no** (detected: `LPC5512`)
        * combined: **no** (detected: `LPC5512`)
    * target in top-3:
        * cmsis-svd-data: **series only**
        * Keil: **no**
        * combined: **no**
* `firmware-xg24.hex`
    * actual target:
        * architecture: `Silicon Labs EFR32xG24`
        * series: `Silicon Labs EFR32xG`
    * target identified:
        * cmsis-svd-data: **no** (detected: `ht32f175x`) *only series in database*
        * Keil: **yes**
        * combined: **yes**
    * target in top-3:
        * cmsis-svd-data: **no**
        * Keil: **yes**
        * combined: **yes**
* `DISCO-L475VG-IOT01A.bin`
    * actual target:
        * architecture: `STM32L475VG`
        * series: `STM32L4`
    * target identified:
        * cmsis-svd-data: **series only** (detected: `STM32L4x3`)
        * Keil: **no** (detected: `BAT32G137A`)
        * combined: **no** (detected: `BAT32G137A`)
    * target in top-3:
        * cmsis-svd-data: **yes**
        * Keil: **no**
        * combined: **no**
* `firmware-st-stm32n6.bin`
    * actual target:
        * architecture: `STM32N6570`
        * series: `STM32N6`
    * target identified:
        * cmsis-svd-data: *series not in database*
        * Keil: **series only**
        * combined: **series only**
    * target in top-3:
        * cmsis-svd-data: *series not in database*
        * Keil: **yes**
        * combined: **yes**

## Statistics

### How many surveyed binaries are covered by the knowledge base?
In total, we surveyed 53 firmware binaries from the Fuzzware sample and the Edge Impulse repositories. Out of these, 36 binaries (68%) target MCUs that are represented in our knowledge base, and 43 binaries (81%) target MCUs whose series is represented in our knowledge base.

### How well can we identify the target architecture of a binary?
Out of the 43 binaries whose target architecture series is represented in our combined knowledge base, we were able to obtain 42 binaries.

#### CMSIS-SVD-Data knowledge base
26 of the obtained binaries target MCUs that are represented in the `cmsis-svd-data` knowledge base. Out of these 26 binaries, we correctly identified the exact target architecture for 10 binaries (38%). For 16 binaries (62%), the exact architecture was in the top-3 highest-ranked results.

#### Keil knowledge base
24 of the obtained binaries target MCUs that are represented in the Keil knowledge base. Out of these 24 binaries, we correctly identified the exact target architecture for 10 binaries (42%). For 13 binaries (54%), the exact architecture was in the top-3 highest-ranked results.

#### Combined knowledge base
34 of the obtained binaries target MCUs that are represented in our combined knowledge base. Out of these 34 binaries, we correctly identified the exact target architecture for 15 binaries (44%). For 20 binaries (59%), the exact architecture was in the top-3 highest-ranked results.

### How well can we identify the target architecture series of a binary?
Out of the 43 binaries whose target architecture series is represented in our combined knowledge base, we were able to obtain 42 binaries.

#### CMSIS-SVD-Data knowledge base
37 of the obtained binaries target MCU series that are represented in the `cmsis-svd-data` knowledge base. Out of these 37 binaries, we correctly identified the target architecture series for 23 binaries (62%). For 28 binaries (76%), the correct architecture series was in the top-3 highest-ranked results.

#### Keil knowledge base
32 of the obtained binaries target MCU series that are represented in the Keil knowledge base. Out of these 32 binaries, we correctly identified the target architecture series for 18 binaries (56%). For 24 binaries (75%), the correct architecture series was in the top-3 highest-ranked results.

#### Combined knowledge base
All 42 obtained binaries target MCU series that are represented in our combined knowledge base. Out of these 42 binaries, we correctly identified the target architecture series for 24 binaries (57%). For 28 binaries (67%), the correct architecture series was in the top-3 highest-ranked results.

# References

[1] Scharnowski, Tobias, et al. "Fuzzware: Using precise MMIO modeling for effective firmware fuzzing." 31st USENIX Security Symposium (USENIX Security 22). 2022.