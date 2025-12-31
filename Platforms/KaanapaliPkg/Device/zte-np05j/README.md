# ZTE PQ84P01 (np05j) - Device Port for UEFI

## Device Information
- **Manufacturer**: ZTE
- **Product Code**: PQ84P01
- **Internal Name**: np05j
- **SoC**: Qualcomm SM8750 (Kera/Pakala platform)
- **Using Silicon**: SM8850 (SM8750 not yet available)

## Current Port Status

### ✅ Completed
1. Device directory structure created
2. Basic configuration files set up
3. DeviceTreeBlob directory structure (Android/Linux subdirs)
4. MLVM enabled in Defines.dsc.inc
5. Display resolution configured (placeholder: 1080x2400)
6. Binaries and PatchedBinaries directories cleaned and ready

### ⚠️ Critical Missing Components

#### 1. Firmware Binaries (REQUIRED)
**Status:** ❌ Not extracted yet

The `Binaries/` directory is empty and requires firmware components extracted from the device's UEFI image.

**Action Required:**
```bash
# Download and compile UefiReader from:
# https://github.com/WOA-Project/UEFIReader

# Extract binaries (assuming you have np05j/uefi_a.img):
UefiReader np05j/uefi_a.img Platforms/KaanapaliPkg/Device/zte-np05j/Binaries/
```

#### 2. Device Tree Blob
**Status:** ⚠️ Placeholders only

**Action Required:**
Get the actual Android DTB from your device:
```bash
# Method 1: From running device
adb shell su -c "cp /sys/firmware/fdt /sdcard/fdt"
adb pull /sdcard/fdt DeviceTreeBlob/Android/android-np05j.dtb

# Method 2: Extract from boot.img
# Download magiskboot, then:
magiskboot unpack boot.img
mv kernel_dtb DeviceTreeBlob/Android/android-np05j.dtb
```

#### 3. DXE Configuration Files
**Status:** ❌ Not created yet

After extracting binaries with UefiReader, you'll need to:
1. Review and edit `APRIORI.inc` (driver load order)
2. Review and edit `DXE.inc` (driver includes and resources)
3. Review and edit `DXE.dsc.inc` (driver declarations)

## Build Instructions

**⚠️ Warning:** Cannot build until binaries are extracted!

Once binaries are in place:
```bash
# Initialize build environment (first time only)
./build_setup.sh
pip install --upgrade -r pip-requirements.txt
./build_uefi.py --init

# Build UEFI firmware
./build_uefi.py -d zte-np05j -t DEBUG
```

## Configuration Details

### Display (Placeholder Values)
- **Resolution**: 1080x2400 ⚠️ **VERIFY THIS**
- **Console**: 135x126 characters

### SMBIOS
- **Brand**: ZTE
- **Model**: PQ84P01
- **Board**: np05j
- **ABL Product**: kera

### Build Settings
- **MLVM**: Enabled (TRUE)
  - Set to avoid MLVM issues during early testing
  - Can be disabled (FALSE) once Windows boots to save ~300MB RAM

## Next Steps

See [NEXT_STEPS.md](./NEXT_STEPS.md) for detailed instructions on:
1. Extracting firmware binaries with UefiReader
2. Obtaining device tree blobs
3. Configuring DXE files
4. Building and testing
5. Debugging common issues

## Reference Documentation

- **SimpleGuide.md**: Full porting guide in Documentation/
- **DefinesGuidance.md**: Macros and defines reference
- **NEXT_STEPS.md**: Detailed next steps for this device

## Known Limitations

1. **Using SM8850 instead of SM8750**
   - SM8750 silicon package does not exist yet
   - Using SM8850 as it's the closest available
   - May have differences in memory map, peripherals, clocks

2. **RUMI Firmware Source**
   - Source firmware from RUMI (pre-silicon emulation)
   - May differ from actual silicon
   - Some configurations might be emulation-specific

3. **Placeholder Values**
   - Display resolution needs verification
   - Memory configuration may need adjustment
   - Hardware button GPIO mappings unknown

## Troubleshooting

If you encounter errors:

**"Binaries not found" during build:**
- Extract binaries from uefi_a.img using UefiReader

**Build fails with missing includes:**
- Ensure DXE files are created after binary extraction

**Cannot find UefiReader:**
- Download from https://github.com/WOA-Project/UEFIReader
- Compile according to repository instructions

## Contributing

When you successfully boot UEFI:
1. Document display resolution and hardware specs
2. Share memory map configurations
3. Note any binary patches needed
4. Update this README with actual values

## License

Follows mu_aloha_platforms repository license
