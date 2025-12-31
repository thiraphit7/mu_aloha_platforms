# แผนการ Porting np05j ไปยัง mu_aloha_platforms

## Overview

เอกสารนี้เป็นแผนการทำงานแบบ step-by-step สำหรับการ port ZTE device (np05j)
ที่ใช้ SM8750 SoC เข้าสู่ mu_aloha_platforms repository

## Pre-requisites

### 1. ตัดสินใจเลือกชื่อ
**คำถาม:** ควรใช้ชื่อ package ว่าอะไร?

**ตัวเลือก:**
- [x] **KeraPkg** - ตามชื่อใน Device Tree (แนะนำ)
- [ ] **PakalaPkg** - ตามชื่อใน build path
- [ ] **Np05jPkg** - ตามโฟลเดอร์ปัจจุบัน

**เหตุผล:** Kera เป็นชื่อที่ปรากฏใน Device Tree และสอดคล้องกับ naming convention

### 2. ตัดสินใจชื่อ Device Target
**คำถาม:** ควรใช้ชื่อ device target ว่าอะไร?

**ตัวเลือก:**
- [ ] `zte-np05j` - ตาม folder name
- [x] `zte-pq84p01` - ตาม product code (แนะนำ)
- [ ] `zte-kera` - ตาม platform name

**เหตุผล:** PQ84P01 เป็น product code ที่ชัดเจนกว่า

---

## Phase 1: สร้าง SM8750 Silicon Support

### Step 1.1: สร้าง Silicon Package Directory
```bash
mkdir -p Silicon/QC/Sm8750/QcomPkg/Include
mkdir -p Silicon/QC/Sm8750/QcomPkg/Library
```

### Step 1.2: คัดลอกไฟล์ฐานจาก SM8850
```bash
cp -r Silicon/QC/Sm8850/QcomPkg/* Silicon/QC/Sm8750/QcomPkg/
```

### Step 1.3: แก้ไข QcomPkg.dec
**ไฟล์:** `Silicon/QC/Sm8750/QcomPkg/QcomPkg.dec`

```diff
[Defines]
  DEC_SPECIFICATION              = 0x00010005
  PACKAGE_NAME                   = QcomPkg
- PACKAGE_GUID                   = 5fd522a5-b671-429f-957f-75113dd02430
+ PACKAGE_GUID                   = [GENERATE NEW GUID]
  PACKAGE_VERSION                = 0.1
```

**Action:** Generate new GUID using `uuidgen` command

### Step 1.4: ปรับแต่ง Include Headers
**ไฟล์ที่ต้องตรวจสอบ:**
- `Include/Configuration/BootDevices.h`
- `Include/Configuration/DeviceMemoryMap.h`
- `Include/Library/PlatformMemoryMapLib.h`

**Note:** จะต้องอัปเดต memory addresses ตาม SM8750 specification

### Step 1.5: อัปเดต Library Implementations
**ไฟล์:** Libraries ต่างๆ ใน `Silicon/QC/Sm8750/QcomPkg/Library/`

**ความแตกต่างที่คาดว่าจะมี:**
- Base addresses สำหรับ peripherals
- Clock configurations
- Power domain settings
- Memory map

**Action:** ตอนนี้คัดลอกจาก SM8850 ก่อน, จะปรับแต่งทีหลังเมื่อมีข้อมูลมากขึ้น

---

## Phase 2: สร้าง Platform Package (KeraPkg)

### Step 2.1: สร้าง Package Directory Structure
```bash
mkdir -p Platforms/KeraPkg/Device/zte-pq84p01
mkdir -p Platforms/KeraPkg/Include
mkdir -p Platforms/KeraPkg/PythonLibs
```

### Step 2.2: สร้าง Device Directory Structure
```bash
cd Platforms/KeraPkg/Device/zte-pq84p01
mkdir ACPI
mkdir Binaries
mkdir DeviceTreeBlob
mkdir Library
mkdir PatchedBinaries
mkdir -p Library/PlatformMemoryMapLib
mkdir -p Library/PlatformConfigurationMapLib
```

### Step 2.3: คัดลอกไฟล์เทมเพลตจาก KaanapaliPkg
```bash
# Copy package-level files
cp Platforms/KaanapaliPkg/KeraPkg.dec Platforms/KeraPkg/
cp Platforms/KaanapaliPkg/Kaanapali.dsc Platforms/KeraPkg/Kera.dsc
cp Platforms/KaanapaliPkg/Kaanapali.fdf Platforms/KeraPkg/Kera.fdf
cp Platforms/KaanapaliPkg/KaanapaliNoSb.dsc Platforms/KeraPkg/KeraNoSb.dsc
cp Platforms/KaanapaliPkg/PlatformBuild.py Platforms/KeraPkg/
cp Platforms/KaanapaliPkg/PlatformBuildNoSb.py Platforms/KeraPkg/

# Copy device-level files
cp -r Platforms/KaanapaliPkg/Device/oneplus-plk110/* \
      Platforms/KeraPkg/Device/zte-pq84p01/
```

### Step 2.4: สร้าง KeraPkg.dec
**ไฟล์:** `Platforms/KeraPkg/KeraPkg.dec`

```ini
[Defines]
  DEC_SPECIFICATION              = 0x00010005
  PACKAGE_NAME                   = KeraPkg
  PACKAGE_GUID                   = [GENERATE NEW GUID]
  PACKAGE_VERSION                = 0.1

[Includes.common]
  Include
```

**Action:** Run `uuidgen` to generate new GUID

### Step 2.5: แก้ไข Kera.dsc
**ไฟล์:** `Platforms/KeraPkg/Kera.dsc`

**Changes needed:**
```ini
[Defines]
  PLATFORM_NAME                  = Kera
  PLATFORM_GUID                  = [GENERATE NEW GUID]
  PLATFORM_VERSION               = 0.1
  DSC_SPECIFICATION              = 0x00010005
  OUTPUT_DIRECTORY               = Build/KeraPkg
  SUPPORTED_ARCHITECTURES        = AARCH64
  BUILD_TARGETS                  = DEBUG|RELEASE
  SKUID_IDENTIFIER               = DEFAULT
  PACKAGE_NAME                   = KeraPkg
  FLASH_DEFINITION               = KeraPkg/Kera.fdf
  SECURE_BOOT                    = 1
  USE_PHYSICAL_TIMER             = 0

  USE_SCREEN_FOR_SERIAL_OUTPUT    = 0
  USE_UART_GENI_FOR_SERIAL_OUTPUT = 0
  USE_UART_DM_FOR_SERIAL_OUTPUT   = 0
  USE_MEMORY_FOR_SERIAL_OUTPUT    = 0

  # ... (secure boot keys - keep same as KaanapaliPkg)

  # Platform-specific errata flags (may need adjustment for SM8750)
  PLATFORM_HAS_ACTLR_EL1_UNIMPLEMENTED_ERRATA         = 0
  PLATFORM_HAS_AMCNTENSET0_EL0_UNIMPLEMENTED_ERRATA   = 1
  PLATFORM_HAS_GIC_V3_WITHOUT_IRM_FLAG_SUPPORT_ERRATA = 0
  PLATFORM_HAS_PSCI_MEMPROTECT_FAILING_ERRATA         = 0

!include KeraPkg/Device/$(TARGET_DEVICE)/Defines.dsc.inc

[PcdsFixedAtBuild.common]
  # Platform-specific
  gArmTokenSpaceGuid.PcdSystemMemorySize|0x300000000        # 12GB - MAY NEED ADJUSTMENT

  gAndromedaPkgTokenSpaceGuid.PcdABLProduct|"Kera"

[Components.common]
  AndromedaPkg/Driver/SimpleFbDxe/SimpleFbDxe.inf

[LibraryClasses.common]
  PlatformMemoryMapLib|KeraPkg/Device/$(TARGET_DEVICE)/Library/PlatformMemoryMapLib/PlatformMemoryMapLib.inf
  PlatformConfigurationMapLib|KeraPkg/Device/$(TARGET_DEVICE)/Library/PlatformConfigurationMapLib/PlatformConfigurationMapLib.inf

!include KeraPkg/Device/$(TARGET_DEVICE)/DXE.dsc.inc
!include QcomPkg/QcomPkg.dsc.inc
!include KeraPkg/Device/$(TARGET_DEVICE)/PcdsFixedAtBuild.dsc.inc
!include AndromedaPkg/Andromeda.dsc.inc
!include AndromedaPkg/Frontpage.dsc.inc
```

### Step 2.6: แก้ไข Kera.fdf
**ไฟล์:** `Platforms/KeraPkg/Kera.fdf`

**Changes needed:**
- Update package name references: `KaanapaliPkg` → `KeraPkg`
- Update platform name: `Kaanapali` → `Kera`
- Check memory layout (may need adjustment for SM8750)

### Step 2.7: แก้ไข PlatformBuild.py
**ไฟล์:** `Platforms/KeraPkg/PlatformBuild.py`

**Changes needed:**
```python
# Search and replace:
# "KaanapaliPkg" → "KeraPkg"
# "Kaanapali" → "Kera"
```

**Key sections to verify:**
- Package name
- Platform name
- Build output directory
- DSC file path

---

## Phase 3: Configure Device-Specific Files

### Step 3.1: Defines.dsc.inc
**ไฟล์:** `Platforms/KeraPkg/Device/zte-pq84p01/Defines.dsc.inc`

**Content:** (อาจเว้นว่างไว้หรือเพิ่ม defines พิเศษ)
```ini
# Device-specific build defines
# Currently empty - add custom defines here if needed
```

### Step 3.2: PcdsFixedAtBuild.dsc.inc
**ไฟล์:** `Platforms/KeraPkg/Device/zte-pq84p01/PcdsFixedAtBuild.dsc.inc`

**Content:**
```ini
[PcdsFixedAtBuild.common]
# Display - NEED TO FIND ACTUAL RESOLUTION
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|1080   # PLACEHOLDER
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|2400  # PLACEHOLDER

# Display Caller (uncomment if needed)
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerExitDisableDisplay|FALSE
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerStallBeforeEnable|1000

# Smbios Info
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemBrand|"ZTE"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailSku|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailModel|"ZTE Device"  # NEED REAL NAME
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemModel|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosBoardModel|"Kera"

gAndromedaPkgTokenSpaceGuid.PcdABLProduct|"kera"

[PcdsDynamicDefault.common]
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoHorizontalResolution|1080   # PLACEHOLDER
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoVerticalResolution|2400     # PLACEHOLDER
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoHorizontalResolution|1080
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoVerticalResolution|2400
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutColumn|135  # = 1080 / 8
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutRow|126     # = 2400 / 19
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutColumn|135
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutRow|126
```

**TODO:** Find actual display resolution from device specs

### Step 3.3: DXE.dsc.inc และ DXE.inc
**Action:** คัดลอกจาก KaanapaliPkg แล้วตรวจสอบ

**ไฟล์:**
- `Platforms/KeraPkg/Device/zte-pq84p01/DXE.dsc.inc`
- `Platforms/KeraPkg/Device/zte-pq84p01/DXE.inc`

**Verification needed:**
- Binary paths pointing to correct locations
- Driver INF files are correct

### Step 3.4: APRIORI.inc
**Action:** คัดลอกจาก KaanapaliPkg

**ไฟล์:** `Platforms/KeraPkg/Device/zte-pq84p01/APRIORI.inc`

**Note:** กำหนดลำดับการโหลด DXE drivers

---

## Phase 4: Process Binaries

### Step 4.1: Extract Device Tree
```bash
# Install dtc if not available
sudo apt-get install device-tree-compiler

# Try to extract DTB from DTBO
# Note: DTBO may need special handling
dtc -I dtb -O dts -o np05j/kera.dts np05j/dtbo_a.img 2>/dev/null || \
  echo "DTBO extraction may need manual processing"
```

**Expected output:** `.dts` file with device tree source

**Analyze for:**
- Memory regions
- Peripheral addresses
- GPIO configurations
- Display panel info
- Device identifiers

### Step 4.2: Copy DTBO to DeviceTreeBlob
```bash
cp np05j/dtbo_a.img \
   Platforms/KeraPkg/Device/zte-pq84p01/DeviceTreeBlob/
```

### Step 4.3: Handle XBL Binary
**Note:** XBL binary จาก stock firmware ไม่ได้ใช้ตรงๆ

**Options:**
1. Use for reference/analysis only
2. Extract useful information (memory map, etc.)
3. May not need to include in repository

### Step 4.4: Handle UEFI Binary
**ไฟล์:** `np05j/uefi_a.img`

**Analysis:**
```bash
# Check entry point
readelf -h np05j/uefi_a.img | grep "Entry point"

# Check sections
readelf -S np05j/uefi_a.img

# Extract strings for useful info
strings np05j/uefi_a.img > np05j/uefi_strings.txt
```

**Use case:** Reference for comparing with our built UEFI

---

## Phase 5: Create Libraries

### Step 5.1: PlatformMemoryMapLib
**Directory:** `Platforms/KeraPkg/Device/zte-pq84p01/Library/PlatformMemoryMapLib/`

**Files needed:**
```
PlatformMemoryMapLib/
├── PlatformMemoryMapLib.c
├── PlatformMemoryMapLib.h
└── PlatformMemoryMapLib.inf
```

**Action:**
1. Copy from KaanapaliPkg device
2. Update memory regions based on SM8750 specs
3. Adjust for device-specific memory layout

**Critical areas to update:**
- RAM_PARTITION_NAME defines
- Memory region base addresses
- Memory region sizes
- Reserved memory regions

### Step 5.2: PlatformConfigurationMapLib
**Directory:** `Platforms/KeraPkg/Device/zte-pq84p01/Library/PlatformConfigurationMapLib/`

**Files needed:**
```
PlatformConfigurationMapLib/
├── PlatformConfigurationMapLib.c
└── PlatformConfigurationMapLib.inf
```

**Action:**
1. Copy from KaanapaliPkg device
2. Update device configurations:
   - GPIO mappings (Power button, Volume buttons)
   - PMIC configuration
   - USB configuration
   - Display configuration

---

## Phase 6: Create Build Configuration

### Step 6.1: สร้าง build_cfg/sm8750.json
**ไฟล์:** `build_cfg/sm8750.json`

```json
{
    "platform": "Sm8750",
    "package": "KeraPkg",
    "bootshim": {
        "UEFI_BASE": "0xFF300000",
        "UEFI_SIZE": "0x00400000"
    }
}
```

**Note:** UEFI_BASE และ UEFI_SIZE อาจต้องปรับตามข้อมูลจริง

### Step 6.2: สร้าง devices.json entry
**ไฟล์:** ตรวจสอบว่ามี `devices.json` หรือ configuration file อื่นหรือไม่

**Content example:**
```json
{
    "zte-pq84p01": {
        "platform": "Sm8750",
        "package": "KeraPkg",
        "manufacturer": "ZTE",
        "model": "PQ84P01"
    }
}
```

---

## Phase 7: Update Documentation

### Step 7.1: สร้าง README.md ใน KeraPkg
**ไฟล์:** `Platforms/KeraPkg/README.md`

```markdown
# KeraPkg - SM8750 Platform Package

## Overview
Platform package for devices using Qualcomm SM8750 SoC (Kera platform).

## Supported Devices
- ZTE PQ84P01 (`zte-pq84p01`)

## Build Instructions
\`\`\`bash
./build_uefi.py -d zte-pq84p01
\`\`\`

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
- Display resolution is placeholder

## Contributing
[Information about how to contribute]
```

### Step 7.2: อัปเดต README.md หลัก
**ไฟล์:** `README.md`

**Add to device list:**
```markdown
### Snapdragon 8 Gen 5+ (*SM8750*)

#### ZTE Devices
| Device                               | Target name            | DSDT Support    | Contributors                                       |
|--------------------------------------|------------------------|-----------------|----------------------------------------------------|
| ZTE PQ84P01                          | zte-pq84p01            | ❌              | [Your Name]                                        |
```

---

## Phase 8: Initial Build และ Test

### Step 8.1: Initialize Build Environment
```bash
./build_setup.sh
pip install --upgrade -r pip-requirements.txt
./build_uefi.py --init
```

### Step 8.2: Attempt First Build
```bash
./build_uefi.py -d zte-pq84p01 -t DEBUG
```

### Step 8.3: Expected Issues และ Solutions

**Issue 1: Missing QcomPkg.dsc.inc for SM8750**
**Solution:**
- Create `Silicon/QC/Sm8750/QcomPkg/QcomPkg.dsc.inc`
- Copy from SM8850 and adjust

**Issue 2: Missing binary files**
**Solution:**
- Check Binaries/ directory structure
- Ensure all referenced .inf files exist
- May need to adjust DXE.inc to remove missing binaries

**Issue 3: GUID conflicts**
**Solution:**
- Ensure all GUIDs are unique
- Use `uuidgen` to generate new ones

**Issue 4: Memory map errors**
**Solution:**
- Review PlatformMemoryMapLib implementation
- Check for syntax errors
- Verify memory region definitions

**Issue 5: Missing include files**
**Solution:**
- Verify all include paths
- Check that Silicon/QC/Sm8750 structure is complete

### Step 8.4: Build Troubleshooting Commands
```bash
# Clean build
rm -rf Build/KeraPkg

# Verbose build
./build_uefi.py -d zte-pq84p01 -t DEBUG --verbose

# Check for syntax errors in .dsc
stuart_parse -c Platforms/KeraPkg/Kera.dsc

# Check .fdf
stuart_parse -c Platforms/KeraPkg/Kera.fdf
```

---

## Phase 9: Testing Strategy

### Step 9.1: Verify Build Artifacts
**Check for:**
```
Build/KeraPkg/
├── DEBUG_CLANGPDB/ (or RELEASE_CLANGPDB/)
│   ├── AARCH64/
│   │   └── ... (compiled objects)
│   └── FV/
│       └── ... (firmware volumes)
└── zte-pq84p01.img  (final bootable image)
```

### Step 9.2: Analyze Build Output
```bash
# Check image size
ls -lh Build/KeraPkg/zte-pq84p01.img

# Verify it's an Android boot image format
file Build/KeraPkg/zte-pq84p01.img

# Extract boot.img info if needed
# (requires additional tools like unpackbootimg)
```

### Step 9.3: Test Booting (if hardware available)
**Methods:**
1. Fastboot boot (non-permanent test)
   ```bash
   fastboot boot Build/KeraPkg/zte-pq84p01.img
   ```

2. Fastboot flash (permanent)
   ```bash
   fastboot flash boot_a Build/KeraPkg/zte-pq84p01.img
   fastboot reboot
   ```

**Note:** Backup stock boot image first!

### Step 9.4: Expected Behavior
**Success indicators:**
- [ ] Device powers on
- [ ] Display shows output (even if garbled)
- [ ] UEFI menu appears
- [ ] Can navigate menu with buttons

**Common failures:**
- Black screen (display init failed)
- Immediate reboot (critical error)
- Stuck on boot logo (hang during init)
- No response (brick - needs recovery)

### Step 9.5: Debugging Failed Boot
**Serial output (if available):**
- Connect UART/serial cable
- Capture boot logs
- Look for error messages

**Without serial:**
- Check if device vibrates (indicates code execution)
- Check LED patterns
- Try different build configurations

---

## Phase 10: Iterative Improvement

### Step 10.1: Priority Fixes
1. **Display initialization** - Critical for usability
2. **Storage (UFS) support** - Needed for boot
3. **USB support** - For debugging and peripherals
4. **Power management** - For stability

### Step 10.2: Enhancement Roadmap
1. **Short-term (1-2 weeks):**
   - Get basic boot working
   - Display output
   - Button input
   - Storage detection

2. **Medium-term (1-2 months):**
   - ACPI tables
   - Windows boot support
   - USB host mode
   - Battery/charging

3. **Long-term (3+ months):**
   - Full DSDT support
   - Audio support
   - Camera support
   - Optimize performance

---

## Important Notes และ Caveats

### RUMI Platform Warning
- np05j firmware is built for RUMI (pre-silicon emulation)
- May have differences from actual silicon
- Some features may not work on real hardware
- May need adjustments when actual SM8750 silicon specs are available

### Missing Information
**Critical unknowns:**
- Actual display resolution
- Complete memory map for SM8750
- Peripheral base addresses for SM8750
- Device marketing name
- Hardware button GPIO mappings

**Impact:**
- Initial build will use placeholder values
- May not boot on first try
- Will require iteration and testing

### Hardware Requirements for Testing
- ZTE device with SM8750 (if it exists in consumer form)
- OR SM8750 development board
- OR wait for more information about the platform

### Legal Considerations
- Ensure compliance with licenses
- Don't redistribute proprietary binaries without permission
- ZTE firmware binaries are likely proprietary

---

## Success Criteria

### Minimum Viable Port (MVP):
- [ ] Code compiles without errors
- [ ] Generates bootable image
- [ ] Image can be flashed to device
- [ ] Device boots to some recognizable state

### Basic Functionality:
- [ ] UEFI menu displays correctly
- [ ] Can navigate menu with hardware buttons
- [ ] Storage devices detected
- [ ] USB works in some capacity

### Full Functionality:
- [ ] Boots Windows/Linux
- [ ] All hardware working (display, storage, USB, etc.)
- [ ] ACPI/DSDT support
- [ ] Stable and performant

---

## Timeline Estimate

**Week 1-2:** Setup และ Initial Build
- Create package structure
- Configure build files
- First build attempt
- Fix compilation errors

**Week 3-4:** Basic Boot
- Debug boot failures
- Get display working
- Get to UEFI menu

**Week 5-8:** Hardware Support
- Storage (UFS)
- USB
- Power management
- Button input

**Week 9-12:** OS Boot
- ACPI tables
- Windows boot
- Driver integration
- Testing และ bug fixes

**Beyond:** Enhancement และ Optimization

**Note:** Timeline assumes:
- Part-time work (few hours per day)
- Access to hardware for testing
- Availability of SM8750 documentation

---

## Resources และ References

### Internal References:
- `Silicon/QC/Sm8850/` - Most similar SoC
- `Platforms/KaanapaliPkg/` - Most similar platform (also SM8850)
- `build_cfg/sm8850.json` - Build config example

### External Documentation:
- [Project Mu Documentation](https://microsoft.github.io/mu/)
- [EDK2 Documentation](https://github.com/tianocore/tianocore.github.io/wiki)
- [UEFI Specification](https://uefi.org/specifications)
- Qualcomm SM8750 documentation (if available)

### Tools:
- Device Tree Compiler (dtc)
- binwalk
- Android boot image tools
- Serial terminal (minicom, screen, etc.)

---

## Conclusion

การ port np05j เป็นโครงการที่มีความท้าทาย แต่มีโครงสร้างพื้นฐานที่ดีจาก
mu_aloha_platforms ที่สามารถใช้เป็นฐานได้

ความสำเร็จของโครงการนี้ขึ้นอยู่กับ:
1. การเข้าถึง hardware สำหรับทดสอบ
2. ความพร้อมของ SM8750 documentation
3. เวลาและความพยายามในการ debug

แนวทางที่ดีที่สุดคือเริ่มจากสิ่งที่ง่ายที่สุด (compilation) และค่อยๆ แก้ไข
ปัญหาทีละอย่างจนกระทั่งได้ UEFI firmware ที่สามารถใช้งานได้
