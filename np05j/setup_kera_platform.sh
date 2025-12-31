#!/bin/bash
# Script to setup KeraPkg platform structure for ZTE PQ84P01 (np05j)
# Based on SM8750 SoC (Kera/Pakala platform)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PLATFORM_NAME="Kera"
PACKAGE_NAME="KeraPkg"
DEVICE_NAME="zte-pq84p01"
BASE_PLATFORM="KaanapaliPkg"
BASE_DEVICE="oneplus-plk110"
BASE_SOC="Sm8850"
NEW_SOC="Sm8750"

echo -e "${GREEN}=== np05j Platform Setup Script ===${NC}"
echo ""
echo "This script will create:"
echo "  - Silicon/QC/${NEW_SOC}/ (based on ${BASE_SOC})"
echo "  - Platforms/${PACKAGE_NAME}/"
echo "  - Platforms/${PACKAGE_NAME}/Device/${DEVICE_NAME}/"
echo "  - build_cfg/sm8750.json"
echo ""

# Confirm before proceeding
read -p "Do you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

#==============================================================================
# Phase 1: Create SM8750 Silicon Support
#==============================================================================
echo -e "${YELLOW}Phase 1: Creating SM8750 Silicon Support...${NC}"

if [ -d "Silicon/QC/${NEW_SOC}" ]; then
    echo -e "${RED}Warning: Silicon/QC/${NEW_SOC} already exists!${NC}"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "Silicon/QC/${NEW_SOC}"
    else
        echo "Skipping Silicon package creation."
    fi
fi

if [ ! -d "Silicon/QC/${NEW_SOC}" ]; then
    echo "Creating Silicon/QC/${NEW_SOC}/..."
    mkdir -p "Silicon/QC/${NEW_SOC}/QcomPkg"

    echo "Copying from ${BASE_SOC}..."
    cp -r "Silicon/QC/${BASE_SOC}/QcomPkg"/* "Silicon/QC/${NEW_SOC}/QcomPkg/"

    # Generate new GUID for QcomPkg.dec
    NEW_GUID=$(uuidgen)
    echo "Updating GUID in QcomPkg.dec to ${NEW_GUID}..."
    sed -i "s/PACKAGE_GUID.*=.*/PACKAGE_GUID                   = ${NEW_GUID}/" \
        "Silicon/QC/${NEW_SOC}/QcomPkg/QcomPkg.dec"

    echo -e "${GREEN}✓ SM8750 Silicon package created${NC}"
else
    echo -e "${YELLOW}Silicon package already exists, skipping.${NC}"
fi

#==============================================================================
# Phase 2: Create Platform Package
#==============================================================================
echo -e "${YELLOW}Phase 2: Creating ${PACKAGE_NAME} Platform Package...${NC}"

if [ -d "Platforms/${PACKAGE_NAME}" ]; then
    echo -e "${RED}Warning: Platforms/${PACKAGE_NAME} already exists!${NC}"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "Platforms/${PACKAGE_NAME}"
    else
        echo "Skipping Platform package creation."
        exit 1
    fi
fi

echo "Creating Platforms/${PACKAGE_NAME}/..."
mkdir -p "Platforms/${PACKAGE_NAME}"
mkdir -p "Platforms/${PACKAGE_NAME}/Include"
mkdir -p "Platforms/${PACKAGE_NAME}/PythonLibs"

echo "Copying base files from ${BASE_PLATFORM}..."

# Copy and rename .dec file
cp "Platforms/${BASE_PLATFORM}/${BASE_PLATFORM}.dec" \
   "Platforms/${PACKAGE_NAME}/${PACKAGE_NAME}.dec"

# Generate new GUID for package
PKG_GUID=$(uuidgen)
echo "Updating GUID in ${PACKAGE_NAME}.dec to ${PKG_GUID}..."
sed -i "s/PACKAGE_NAME.*=.*/PACKAGE_NAME                   = ${PACKAGE_NAME}/" \
    "Platforms/${PACKAGE_NAME}/${PACKAGE_NAME}.dec"
sed -i "s/PACKAGE_GUID.*=.*/PACKAGE_GUID                   = ${PKG_GUID}/" \
    "Platforms/${PACKAGE_NAME}/${PACKAGE_NAME}.dec"

# Copy and process .dsc files
for dsc_file in Platforms/${BASE_PLATFORM}/*.dsc; do
    base_name=$(basename "$dsc_file")
    new_name="${base_name/Kaanapali/${PLATFORM_NAME}}"

    echo "Creating ${new_name}..."
    cp "$dsc_file" "Platforms/${PACKAGE_NAME}/${new_name}"

    # Update package references
    sed -i "s/${BASE_PLATFORM}/${PACKAGE_NAME}/g" "Platforms/${PACKAGE_NAME}/${new_name}"
    sed -i "s/Kaanapali/${PLATFORM_NAME}/g" "Platforms/${PACKAGE_NAME}/${new_name}"

    # Generate new GUID for main .dsc
    if [[ "$new_name" == "${PLATFORM_NAME}.dsc" ]]; then
        DSC_GUID=$(uuidgen)
        echo "Updating PLATFORM_GUID to ${DSC_GUID}..."
        sed -i "s/PLATFORM_GUID.*=.*/PLATFORM_GUID                  = ${DSC_GUID}/" \
            "Platforms/${PACKAGE_NAME}/${new_name}"
    fi
done

# Copy and process .fdf files
for fdf_file in Platforms/${BASE_PLATFORM}/*.fdf; do
    base_name=$(basename "$fdf_file")
    new_name="${base_name/Kaanapali/${PLATFORM_NAME}}"

    echo "Creating ${new_name}..."
    cp "$fdf_file" "Platforms/${PACKAGE_NAME}/${new_name}"

    # Update package references
    sed -i "s/${BASE_PLATFORM}/${PACKAGE_NAME}/g" "Platforms/${PACKAGE_NAME}/${new_name}"
    sed -i "s/Kaanapali/${PLATFORM_NAME}/g" "Platforms/${PACKAGE_NAME}/${new_name}"
done

# Copy and process Python build scripts
echo "Copying PlatformBuild.py..."
cp "Platforms/${BASE_PLATFORM}/PlatformBuild.py" \
   "Platforms/${PACKAGE_NAME}/PlatformBuild.py"
sed -i "s/${BASE_PLATFORM}/${PACKAGE_NAME}/g" \
    "Platforms/${PACKAGE_NAME}/PlatformBuild.py"
sed -i "s/Kaanapali/${PLATFORM_NAME}/g" \
    "Platforms/${PACKAGE_NAME}/PlatformBuild.py"

echo "Copying PlatformBuildNoSb.py..."
cp "Platforms/${BASE_PLATFORM}/PlatformBuildNoSb.py" \
   "Platforms/${PACKAGE_NAME}/PlatformBuildNoSb.py"
sed -i "s/${BASE_PLATFORM}/${PACKAGE_NAME}/g" \
    "Platforms/${PACKAGE_NAME}/PlatformBuildNoSb.py"
sed -i "s/Kaanapali/${PLATFORM_NAME}/g" \
    "Platforms/${PACKAGE_NAME}/PlatformBuildNoSb.py"

# Copy PythonLibs if they exist
if [ -d "Platforms/${BASE_PLATFORM}/PythonLibs" ]; then
    echo "Copying PythonLibs..."
    cp -r "Platforms/${BASE_PLATFORM}/PythonLibs"/* \
          "Platforms/${PACKAGE_NAME}/PythonLibs/" 2>/dev/null || true
fi

echo -e "${GREEN}✓ ${PACKAGE_NAME} package created${NC}"

#==============================================================================
# Phase 3: Create Device Configuration
#==============================================================================
echo -e "${YELLOW}Phase 3: Creating Device Configuration for ${DEVICE_NAME}...${NC}"

DEVICE_PATH="Platforms/${PACKAGE_NAME}/Device/${DEVICE_NAME}"
echo "Creating ${DEVICE_PATH}..."

mkdir -p "${DEVICE_PATH}"
mkdir -p "${DEVICE_PATH}/ACPI"
mkdir -p "${DEVICE_PATH}/Binaries"
mkdir -p "${DEVICE_PATH}/DeviceTreeBlob"
mkdir -p "${DEVICE_PATH}/Library/PlatformMemoryMapLib"
mkdir -p "${DEVICE_PATH}/Library/PlatformConfigurationMapLib"
mkdir -p "${DEVICE_PATH}/PatchedBinaries"

echo "Copying device files from ${BASE_DEVICE}..."
cp -r "Platforms/${BASE_PLATFORM}/Device/${BASE_DEVICE}"/* "${DEVICE_PATH}/"

# Update PcdsFixedAtBuild.dsc.inc with ZTE-specific info
echo "Updating PcdsFixedAtBuild.dsc.inc..."
cat > "${DEVICE_PATH}/PcdsFixedAtBuild.dsc.inc" << 'EOF'
[PcdsFixedAtBuild.common]
# Display - PLACEHOLDER VALUES - NEED ACTUAL SPECS
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|1080
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|2400

# Display Caller (uncomment if needed)
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerExitDisableDisplay|FALSE
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerStallBeforeEnable|1000

# Smbios Info
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemBrand|"ZTE"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailSku|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailModel|"ZTE PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemModel|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosBoardModel|"Kera"

gAndromedaPkgTokenSpaceGuid.PcdABLProduct|"kera"

[PcdsDynamicDefault.common]
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoHorizontalResolution|1080
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoVerticalResolution|2400
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoHorizontalResolution|1080
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoVerticalResolution|2400
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutColumn|135  # = 1080 / 8
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutRow|126     # = 2400 / 19
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutColumn|135
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutRow|126
EOF

# Create empty Defines.dsc.inc
echo "Creating Defines.dsc.inc..."
cat > "${DEVICE_PATH}/Defines.dsc.inc" << 'EOF'
# Device-specific build defines
# Add custom defines here if needed
EOF

# Copy DTBO to DeviceTreeBlob
if [ -f "np05j/dtbo_a.img" ]; then
    echo "Copying DTBO image..."
    cp np05j/dtbo_a.img "${DEVICE_PATH}/DeviceTreeBlob/"
fi

echo -e "${GREEN}✓ Device configuration created${NC}"

#==============================================================================
# Phase 4: Create Build Configuration
#==============================================================================
echo -e "${YELLOW}Phase 4: Creating build configuration...${NC}"

echo "Creating build_cfg/sm8750.json..."
cat > build_cfg/sm8750.json << 'EOF'
{
    "platform": "Sm8750",
    "package": "KeraPkg",
    "bootshim": {
        "UEFI_BASE": "0xFF300000",
        "UEFI_SIZE": "0x00400000"
    }
}
EOF

echo -e "${GREEN}✓ Build configuration created${NC}"

#==============================================================================
# Phase 5: Create Documentation
#==============================================================================
echo -e "${YELLOW}Phase 5: Creating documentation...${NC}"

echo "Creating Platforms/${PACKAGE_NAME}/README.md..."
cat > "Platforms/${PACKAGE_NAME}/README.md" << 'EOF'
# KeraPkg - SM8750 Platform Package

## Overview
Platform package for devices using Qualcomm SM8750 SoC (Kera/Pakala platform).

## Supported Devices
- ZTE PQ84P01 (`zte-pq84p01`)

## Build Instructions
```bash
# Setup environment (first time only)
./build_setup.sh
pip install --upgrade -r pip-requirements.txt
./build_uefi.py --init

# Build UEFI firmware
./build_uefi.py -d zte-pq84p01
```

## Status
- [ ] Boot to UEFI menu
- [ ] Display output
- [ ] Storage (UFS)
- [ ] USB
- [ ] ACPI/DSDT support
- [ ] Windows boot

## Known Issues
- Platform is based on RUMI (pre-silicon) firmware
- Many hardware details still unknown
- Display resolution is placeholder (1080x2400)
- Memory configuration needs verification

## Hardware Information
- **SoC**: Qualcomm SM8750
- **Platform Codename**: Kera / Pakala
- **Manufacturer**: ZTE
- **Product Code**: PQ84P01

## Notes
This port is based on firmware images from a RUMI (pre-silicon emulation)
platform. Some features may not work correctly on actual silicon, and
adjustments may be needed as more information becomes available.

## References
- Based on KaanapaliPkg (SM8850 / OnePlus 15)
- See np05j/ANALYSIS.md for detailed analysis
- See np05j/PORTING_PLAN.md for porting roadmap
EOF

echo -e "${GREEN}✓ Documentation created${NC}"

#==============================================================================
# Summary
#==============================================================================
echo ""
echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo "Created:"
echo "  ✓ Silicon/QC/${NEW_SOC}/"
echo "  ✓ Platforms/${PACKAGE_NAME}/"
echo "  ✓ Platforms/${PACKAGE_NAME}/Device/${DEVICE_NAME}/"
echo "  ✓ build_cfg/sm8750.json"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review and adjust PcdsFixedAtBuild.dsc.inc for correct device specs"
echo "2. Update memory map in PlatformMemoryMapLib"
echo "3. Update device configuration in PlatformConfigurationMapLib"
echo "4. Run: ./build_uefi.py -d ${DEVICE_NAME} -t DEBUG"
echo "5. Debug any build errors"
echo ""
echo -e "${YELLOW}Important Notes:${NC}"
echo "- Display resolution (1080x2400) is a placeholder - verify actual specs"
echo "- Memory configuration may need adjustment"
echo "- Binary files in Binaries/ may need updating for SM8750"
echo "- DTBO has been copied to DeviceTreeBlob/"
echo ""
echo "For detailed information, see:"
echo "  - np05j/ANALYSIS.md"
echo "  - np05j/PORTING_PLAN.md"
echo "  - Platforms/${PACKAGE_NAME}/README.md"
echo ""
