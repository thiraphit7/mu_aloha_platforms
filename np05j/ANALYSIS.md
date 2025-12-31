# การวิเคราะห์ np05j สำหรับการ Porting

## สรุปข้อมูลที่พบ

### 1. ข้อมูล Firmware Images

#### ไฟล์ที่พบใน ./np05j/

| ไฟล์ | ขนาด | ประเภท | รายละเอียด |
|------|------|--------|-----------|
| `xbl_a.img` | 3.6 MB | ELF 32-bit RISC-V | XBL (eXtensible Bootloader) |
| `uefi_a.img` | 5 MB | ELF 64-bit ARM | UEFI Firmware |
| `dtbo_a.img` | 25 MB | Data | Device Tree Blob Overlay |
| `all.md` | 1 byte | Text | ไฟล์ว่าง |

### 2. ข้อมูล Platform

จากการวิเคราะห์ strings ในไฟล์ firmware:

#### จาก xbl_a.img:
```
/home/zte/workspace/PQ84P01_NON_EEA_V_SM8750_TARGET_V_TA_20250430_03_DAILYBUILD/
modem/amss/BOOT.MXF.2.5.1/boot_images/Build/PakalaLAA/Core/RELEASE_CLANG160LINUX/
AARCH64/QcomPkg/XBLCore/XBLCore/DEBUG/Sec.dll
```

**ข้อมูลสำคัญ:**
- **SoC**: SM8750 (Snapdragon 8 Gen 5 หรือรุ่นใหม่กว่า)
- **Platform Codename**: Pakala / PakalaLAA
- **Manufacturer**: ZTE
- **Product Code**: PQ84P01
- **Build Date**: 2025-04-30
- **Bootloader Version**: BOOT.MXF.2.5.1

#### จาก dtbo_a.img:
```
qcom,kera-rumi
qcom,kera
```

**ข้อมูลสำคัญ:**
- **Device Tree Platform**: Kera
- **RUMI**: Pre-silicon emulation platform (อาจเป็น development/test platform)

### 3. สถานะปัจจุบันใน Repository

#### Silicon Support:
- ล่าสุดที่ support: **SM8850** (Snapdragon 8 Elite Gen 5)
- **SM8750** ยังไม่มี support

#### Platform Packages ที่มีอยู่:
- KaanapaliPkg - OnePlus 15 (SM8850)
- WaipioPkg, KonaPkg, etc. (SoCs รุ่นก่อนหน้า)

### 4. ความท้าทายในการ Porting

1. **SM8750 ยังไม่มีใน Repository**
   - ต้องสร้าง Silicon package ใหม่: `Silicon/QC/Sm8750/`
   - ต้องศึกษาความแตกต่างระหว่าง SM8850 และ SM8750

2. **Platform ใหม่ (Kera/Pakala)**
   - ต้องสร้าง Platform package ใหม่
   - ต้องระบุชื่อ package (เช่น KeraPkg, PakalaPkg)

3. **Device ไม่ทราบรายละเอียด**
   - np05j อาจเป็น:
     - รหัสภายในของ ZTE
     - Development board
     - Device รุ่นใหม่ที่ยังไม่เปิดตัว

4. **RUMI Platform**
   - อาจต้องมีการปรับแต่งพิเศษสำหรับ emulation platform
   - อาจมีข้อจำกัดบางอย่างเมื่อเทียบกับ silicon จริง

## แผนการ Porting

### Phase 1: การเตรียมการ (Preparation)

#### 1.1 สร้าง SM8750 Silicon Package
```
Silicon/QC/Sm8750/
├── QcomPkg/
│   ├── QcomPkg.dec
│   ├── QcomPkg.dsc.inc
│   ├── Include/
│   └── Library/
```

**ขั้นตอน:**
- [ ] คัดลอกโครงสร้างจาก `Silicon/QC/Sm8850/`
- [ ] ปรับแต่ง memory map และ configurations
- [ ] อัปเดต GUID และ identifiers

#### 1.2 กำหนดชื่อ Platform Package

**ตัวเลือก:**
1. **KeraPkg** - ใช้ชื่อตาม Device Tree platform
2. **PakalaPkg** - ใช้ชื่อตาม build path codename
3. **Np05jPkg** - ใช้ชื่อตามที่ระบุ

**คำแนะนำ:** ใช้ **KeraPkg** เพราะสอดคล้องกับ naming convention ที่มีอยู่

#### 1.3 สร้าง Platform Package Structure
```
Platforms/KeraPkg/
├── Device/
│   └── zte-np05j/           # หรือชื่อ device ที่เหมาะสม
│       ├── ACPI/
│       ├── Binaries/
│       ├── DeviceTreeBlob/
│       ├── Library/
│       ├── PatchedBinaries/
│       ├── APRIORI.inc
│       ├── DXE.dsc.inc
│       ├── DXE.inc
│       ├── Defines.dsc.inc
│       └── PcdsFixedAtBuild.dsc.inc
├── Include/
├── PythonLibs/
├── Kera.dsc
├── Kera.fdf
├── KeraNoSb.dsc
├── KeraPkg.dec
├── PlatformBuild.py
├── PlatformBuildNoSb.py
└── README.md
```

### Phase 2: การ Port Firmware Binary Files

#### 2.1 จัดระเบียบ Binary Files

**ไฟล์ที่ต้อง integrate:**
- `xbl_a.img` → ไปยัง bootshim
- `uefi_a.img` → ใช้สำหรับ reference/comparison
- `dtbo_a.img` → extract และ convert เป็น .dtb ใน DeviceTreeBlob/

**ขั้นตอน:**
- [ ] Extract DTBO และวิเคราะห์ device tree
- [ ] สร้าง Device Tree Blob configuration
- [ ] Setup bootshim configuration

#### 2.2 สร้าง build_cfg/sm8750.json
```json
{
    "platform": "Sm8750",
    "package": "KeraPkg",
    "bootshim": {
        "UEFI_BASE": "0xFF300000",  // ต้องตรวจสอบค่าที่ถูกต้อง
        "UEFI_SIZE": "0x00400000"   // ต้องตรวจสอบค่าที่ถูกต้อง
    }
}
```

### Phase 3: Configuration Files

#### 3.1 Kera.dsc (Platform Description)
**ข้อมูลที่ต้องกำหนด:**
- PLATFORM_NAME = Kera
- PLATFORM_GUID = (generate ใหม่)
- Memory size configuration
- Display resolution (ต้องหาจาก device spec)
- SMBIOS information:
  - Brand: "ZTE"
  - Model: "PQ84P01" หรือชื่อการตลาด
  - Retail SKU: "np05j" หรือชื่อที่เหมาะสม

#### 3.2 Device-specific Configurations

**PcdsFixedAtBuild.dsc.inc:**
```
[PcdsFixedAtBuild.common]
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|????
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|????

gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemBrand|"ZTE"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailSku|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailModel|"???" # ต้องหาชื่อ
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemModel|"???"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosBoardModel|"???"

gAndromedaPkgTokenSpaceGuid.PcdABLProduct|"kera" # จาก device tree
```

**ข้อมูลที่ขาดหายและต้องหา:**
- Display resolution
- Device marketing name
- Memory configuration details
- GPIO/Button mappings

### Phase 4: Library และ Driver Integration

#### 4.1 PlatformMemoryMapLib
- ต้องสร้าง memory map สำหรับ SM8750
- อ้างอิงจาก SM8850 และปรับแต่ง

#### 4.2 PlatformConfigurationMapLib
- กำหนด hardware configuration
- GPIO, PMIC, และ peripheral mappings

#### 4.3 Required Drivers
ตรวจสอบว่า drivers เหล่านี้ต้องมีการปรับแต่งหรือไม่:
- SimpleFbDxe (Display)
- UFS controller
- USB controller
- Power management
- Clock/Reset controllers

### Phase 5: Testing และ Debugging

#### 5.1 Initial Build Test
```bash
./build_uefi.py -d zte-np05j -t DEBUG
```

#### 5.2 Expected Issues
1. Missing memory map definitions
2. Incorrect peripheral addresses
3. Display initialization issues
4. Boot failures due to incorrect configurations

#### 5.3 Debugging Strategy
- Enable DEBUG build
- Use serial output if available
- Compare with working SM8850 platform
- Check ACPI tables

### Phase 6: Documentation และ Integration

#### 6.1 อัปเดต README.md
เพิ่ม section ใหม่:
```markdown
### Snapdragon 8 Gen 5+ (*SM8750*)

#### ZTE Devices
| Device                               | Target name            | DSDT Support    | Contributors                                       |
|--------------------------------------|------------------------|-----------------|----------------------------------------------------|
| ZTE PQ84P01                          | zte-np05j              | ❌              | [Your Name]                                        |
```

#### 6.2 สร้าง README.md ใน KeraPkg/
อธิบาย:
- Platform overview
- Supported devices
- Known issues
- Build instructions

## ข้อมูลที่ยังต้องการ (Missing Information)

### Critical (จำเป็นต้องหาก่อน porting):
1. **Display Resolution** - จาก device specification
2. **Memory Map** - จาก Qualcomm SM8750 documentation
3. **Peripheral Base Addresses** - จาก SM8750 datasheet
4. **Device Marketing Name** - ชื่อจริงของอุปกรณ์

### Nice-to-have (สามารถหาทีหลังได้):
1. ACPI tables - สำหรับ DSDT support
2. GPIO button mappings
3. Battery/charging configuration
4. Audio codec information

## ขั้นตอนถัดไป (Next Steps)

### Immediate Actions:
1. **ตัดสินใจชื่อ package**: KeraPkg, PakalaPkg, หรือ Np05jPkg
2. **สร้าง SM8750 silicon package** โดยใช้ SM8850 เป็นฐาน
3. **Extract และวิเคราะห์ DTBO** เพื่อหา hardware configuration
4. **ค้นหาข้อมูล device** (marketing name, specifications)

### Medium-term Goals:
1. สร้าง platform package structure
2. เขียน configuration files
3. Build และ test initial firmware
4. Debug และแก้ไขปัญหา

### Long-term Goals:
1. เพิ่ม ACPI/DSDT support
2. Optimize performance
3. Add advanced features
4. Community testing

## เครื่องมือและทรัพยากรที่จำเป็น

### Tools:
- `dtc` (Device Tree Compiler) - สำหรับ extract DTBO
- `binwalk` - สำหรับวิเคราะห์ binary files
- `readelf` - สำหรับวิเคราะห์ ELF files
- `strings` - สำหรับหา strings ใน binary

### Documentation:
- Qualcomm SM8750 datasheet (ถ้าหาได้)
- SM8850 documentation (สำหรับเปรียบเทียบ)
- EDK2/Project Mu documentation
- Device Tree specification

### Reference Platforms:
- `KaanapaliPkg` (SM8850) - ใกล้เคียงที่สุด
- `WaipioPkg` (SM8450)
- `KonaPkg` (SM8250)

## สรุป

การ port np05j เข้า mu_aloha_platforms เป็นงานที่ท้าทายเพราะ:
1. SM8750 เป็น SoC ที่ยังไม่มีใน repository
2. ข้อมูล hardware specification ยังไม่ครบถ้วน
3. Platform เป็น RUMI (emulation) ซึ่งอาจมีข้อจำกัด

อย่างไรก็ตาม มีโครงสร้างพื้นฐานที่ดีจาก SM8850 ที่สามารถนำมาใช้เป็นฐานได้
และมี firmware binaries ที่สามารถนำมาวิเคราะห์เพื่อหา configuration ได้

**แนวทางที่แนะนำ:** เริ่มจากการสร้าง SM8750 silicon package และ
platform package พื้นฐาน จากนั้นค่อยๆ เพิ่ม features และแก้ไขปัญหาที่พบ
