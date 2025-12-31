# ZTE np05j (PQ84P01) - Quick Start Guide

## Prerequisites

You need these firmware files from your device:
1. `uefi_a.img` - UEFI firmware image
2. `dtbo_a.img` - Device Tree Blob Overlay image
3. (Optional) `xbl_a.img` - XBL bootloader for reference

Place these files in a directory (e.g., `firmware/np05j/`).

## Step-by-Step Setup

### 1. Extract UEFI Binaries

```bash
python3 tools/extract_uefi_binaries.py firmware/np05j/uefi_a.img \
    Platforms/KaanapaliPkg/Device/zte-np05j/Binaries/
```

This will populate the `Binaries/` directory with all UEFI drivers and modules.

### 2. Extract Device Tree Blobs

```bash
# Extract all DTBs from DTBO
python3 tools/extract_dtb_from_dtbo.py firmware/np05j/dtbo_a.img \
    temp_dtbs/
```

### 3. Analyze DTBs to Find Display Resolution

```bash
# Analyze each DTB
for dtb in temp_dtbs/*.dtb; do
    echo "========================================
    python3 tools/analyze_dtb.py "$dtb"
done > dtb_analysis.txt

# View the analysis
cat dtb_analysis.txt
```

Look for DTB with:
- Platform: "kera" or "sm8750"
- Display resolution (width x height)
- Memory configuration

### 4. Copy the Correct DTB

```bash
# Find the DTB with "kera" platform (example: dtb_02.dtb)
cp temp_dtbs/dtb_02.dtb \
    Platforms/KaanapaliPkg/Device/zte-np05j/DeviceTreeBlob/Android/android-np05j.dtb
```

### 5. Update Display Resolution

Edit `PcdsFixedAtBuild.dsc.inc` with the actual resolution from DTB analysis:

```ini
# Example: if analysis shows 1440x3168
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|1440
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|3168

gEfiMdeModulePkgTokenSpaceGuid.PcdVideoHorizontalResolution|1440
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoVerticalResolution|3168
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutColumn|180  # = 1440 / 8
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutRow|166     # = 3168 / 19
```

### 6. Create DXE Configuration Files

After binaries are extracted, create these files in the device directory:

#### APRIORI.inc
List drivers that must load first (refer to other devices or SimpleGuide.md).

Example:
```
APRIORI DXE {
  # Critical drivers first
  INF QcomPkg/Drivers/EnvDxe/EnvDxeEnhanced.inf
  INF QcomPkg/Drivers/DALSYSDxe/DALSYSDxe.inf
  INF QcomPkg/Drivers/HWIODxe/HWIODxe.inf
  # ... more drivers
}
```

#### DXE.inc
Include all driver binaries with their resources.

Example:
```
# DXE Drivers
FILE DRIVER = <GUID> {
  SECTION PE32 = Binaries/QcomPkg/Drivers/SomeDriver/SomeDriver.efi
  SECTION UI = "SomeDriver"
}
```

#### DXE.dsc.inc
Declare all drivers for build.

Example:
```
[Components.common]
  Binaries/QcomPkg/Drivers/SomeDriver/SomeDriver.inf
```

**TIP:** Copy and adapt from a similar device (e.g., oneplus-plk110) and adjust GUIDs/paths.

### 7. Configure Memory Map Libraries

You may need to create/update:
- `Library/PlatformMemoryMapLib/PlatformMemoryMapLib.c`
- `Library/PlatformConfigurationMapLib/PlatformConfigurationMapLib.c`

Refer to SM8850 devices for reference, as SM8750 is similar.

### 8. Initial Build

```bash
# First, ensure build environment is initialized
./build_setup.sh
./build_uefi.py --init

# Try to build
./build_uefi.py -d zte-np05j -t DEBUG
```

### 9. Fix Build Errors

Common errors and solutions:

**"File not found" errors:**
- Check paths in DXE.inc and DXE.dsc.inc
- Ensure all referenced binaries exist in Binaries/

**Missing GUIDs:**
- Extract GUIDs from .inf files in Binaries/
- Update APRIORI.inc and DXE.inc with correct GUIDs

**Library errors:**
- May need to implement device-specific libraries
- Copy from similar platform and adapt

### 10. Test Build Output

If build succeeds:
```bash
ls Build/KaanapaliPkg-zte-np05j/DEBUG_CLANG38/FV/
```

Look for:
- `KAANAPALI_UEFI.fd` - The UEFI firmware image
- Other FV (Firmware Volume) files

## Current Status

Based on initial setup:
- ✅ Directory structure created
- ✅ Configuration files (Defines.dsc.inc, PcdsFixedAtBuild.dsc.inc)
- ✅ DeviceTreeBlob structure ready
- ✅ Documentation complete
- ❌ Binaries not extracted (need uefi_a.img)
- ❌ DTB not extracted (need dtbo_a.img)
- ❌ DXE files not created
- ❌ Display resolution placeholder (1080x2400)
- ❌ Memory configuration not verified

## Quick Reference

**Extract binaries:**
```bash
python3 tools/extract_uefi_binaries.py <uefi_image> Platforms/KaanapaliPkg/Device/zte-np05j/Binaries/
```

**Extract DTBs:**
```bash
python3 tools/extract_dtb_from_dtbo.py <dtbo_image> temp_dtbs/
```

**Analyze DTB:**
```bash
python3 tools/analyze_dtb.py <dtb_file>
```

**Build UEFI:**
```bash
./build_uefi.py -d zte-np05j -t DEBUG
```

## Next Steps

1. Obtain firmware images (uefi_a.img, dtbo_a.img)
2. Run extraction scripts
3. Update configuration with actual values
4. Create DXE files
5. Build and test

## Documentation

- **README.md** - Device information and status
- **NEXT_STEPS.md** - Detailed step-by-step instructions
- **USAGE_GUIDE.md** - This file (quick start)
- **tools/README.md** - Tool documentation
- **Documentation/SimpleGuide.md** - Complete porting guide

## Support

For issues or questions:
- Check Documentation/*.md files
- Review similar devices in Platforms/KaanapaliPkg/Device/
- Refer to project issues: https://github.com/Project-Aloha/mu_aloha_platforms/issues
