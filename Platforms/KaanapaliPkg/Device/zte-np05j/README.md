# ZTE PQ84P01 (np05j) Device Configuration

## Device Information
- **Manufacturer**: ZTE
- **Product Code**: PQ84P01
- **Internal Name**: np05j
- **SoC**: Qualcomm SM8750 (using SM8850 platform)
- **Platform**: Kera / Pakala (RUMI)

## Build Instructions
```bash
./build_uefi.py -d zte-np05j
```

For debug build:
```bash
./build_uefi.py -d zte-np05j -t DEBUG
```

## Configuration
- **Display Resolution**: 1080x2400 (placeholder - needs verification)
- **ABL Product**: kera
- **Board Model**: np05j

## Status
- [ ] Initial build
- [ ] Boot to UEFI
- [ ] Display working
- [ ] Storage (UFS)
- [ ] USB
- [ ] Full Windows boot

## Notes
- Based on oneplus-plk110 (SM8850)
- Using SM8850 silicon package
- Firmware source is RUMI (pre-silicon emulation)
- Display resolution is placeholder value

## Source Firmware
- Build: PQ84P01_NON_EEA_V_SM8750_TARGET_V_TA_20250430_03_DAILYBUILD
- Bootloader: BOOT.MXF.2.5.1
- Platform: PakalaLAA

## Known Issues
- Display resolution needs verification from actual device specs
- Memory configuration may need adjustment
- Some binaries may need SM8750-specific versions
