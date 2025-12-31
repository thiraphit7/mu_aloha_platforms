# UEFI Porting Tools

Python scripts for extracting and analyzing firmware binaries for UEFI porting.

## Scripts

### 1. extract_uefi_binaries.py

Python alternative to UEFIReader for extracting UEFI firmware binaries.

**Usage:**
```bash
python3 tools/extract_uefi_binaries.py <uefi_image> <output_dir>
```

**Example:**
```bash
# Extract binaries from uefi_a.img to device Binaries directory
python3 tools/extract_uefi_binaries.py firmware/uefi_a.img \
    Platforms/KaanapaliPkg/Device/zte-np05j/Binaries/
```

**Features:**
- Parses UEFI Firmware File System (FFS) format
- Extracts PE32 (.efi), TE (.te), and RAW (.raw) sections
- Preserves GUID and file type information
- No external dependencies required

### 2. extract_dtb_from_dtbo.py

Extracts Device Tree Blob (DTB) files from Android DTBO images.

**Usage:**
```bash
python3 tools/extract_dtb_from_dtbo.py <dtbo_image> <output_dir>
```

**Example:**
```bash
# Extract DTBs from dtbo_a.img
python3 tools/extract_dtb_from_dtbo.py firmware/dtbo_a.img extracted_dtbs/

# Extract to device Android DTB directory
python3 tools/extract_dtb_from_dtbo.py firmware/dtbo_a.img \
    Platforms/KaanapaliPkg/Device/zte-np05j/DeviceTreeBlob/Android/
```

**Features:**
- Supports Android DTBO format
- Supports raw concatenated DTB format
- Extracts multiple DTBs from single image
- No external dependencies required

### 3. analyze_dtb.py

Analyzes DTB files to extract hardware information including display resolution.

**Usage:**
```bash
python3 tools/analyze_dtb.py <dtb_file>
```

**Example:**
```bash
# Analyze extracted DTB
python3 tools/analyze_dtb.py extracted_dtbs/dtb_00.dtb

# Analyze device Android DTB
python3 tools/analyze_dtb.py \
    Platforms/KaanapaliPkg/Device/zte-np05j/DeviceTreeBlob/Android/android-np05j.dtb
```

**Features:**
- Extracts display resolution (width x height)
- Finds panel compatible strings
- Extracts memory configuration
- Identifies SoC information
- Uses `dtc` (device tree compiler) if available for detailed analysis
- Falls back to string extraction if `dtc` not available

**Dependencies (optional but recommended):**
```bash
sudo apt install device-tree-compiler
```

## Complete Workflow for New Device Port

### Step 1: Obtain Firmware Images

You need these files from your device:
- `uefi_a.img` - UEFI firmware image
- `dtbo_a.img` - Device Tree Blob Overlay image

Extract from device firmware dump or OTA update package.

### Step 2: Extract UEFI Binaries

```bash
# Extract to device Binaries directory
python3 tools/extract_uefi_binaries.py path/to/uefi_a.img \
    Platforms/KaanapaliPkg/Device/<manufacturer>-<codename>/Binaries/
```

This extracts all DXE drivers, applications, and other UEFI modules.

### Step 3: Extract and Analyze DTB

```bash
# Extract DTBs from DTBO
python3 tools/extract_dtb_from_dtbo.py path/to/dtbo_a.img extracted_dtbs/

# Analyze each DTB to find the main one
for dtb in extracted_dtbs/*.dtb; do
    echo "=== Analyzing $dtb ==="
    python3 tools/analyze_dtb.py "$dtb"
done
```

Look for the DTB with:
- Display resolution information
- Memory configuration
- SoC compatible strings matching your device

### Step 4: Copy Correct DTB to Device Directory

```bash
# Copy the correct DTB (e.g., dtb_00.dtb)
cp extracted_dtbs/dtb_00.dtb \
    Platforms/KaanapaliPkg/Device/<manufacturer>-<codename>/DeviceTreeBlob/Android/android-<codename>.dtb
```

### Step 5: Update Device Configuration

Based on analysis output, update these files:

**PcdsFixedAtBuild.dsc.inc:**
```ini
# Update with actual display resolution
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|<width>
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|<height>

# Update console size (width/8, height/19)
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutColumn|<width/8>
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutRow|<height/19>
```

### Step 6: Configure DXE Files

After extracting binaries, you need to create:
- `APRIORI.inc` - DXE driver load order
- `DXE.inc` - Driver includes and resources
- `DXE.dsc.inc` - Driver build declarations

Refer to `Documentation/SimpleGuide.md` for details.

### Step 7: Build UEFI Firmware

```bash
./build_uefi.py -d <manufacturer>-<codename> -t DEBUG
```

Fix any compilation errors that arise.

## Example: ZTE np05j (PQ84P01)

```bash
# 1. Extract binaries
python3 tools/extract_uefi_binaries.py np05j/uefi_a.img \
    Platforms/KaanapaliPkg/Device/zte-np05j/Binaries/

# 2. Extract DTBs
python3 tools/extract_dtb_from_dtbo.py np05j/dtbo_a.img extracted_dtbs/

# 3. Analyze DTBs
for dtb in extracted_dtbs/*.dtb; do
    python3 tools/analyze_dtb.py "$dtb" | tee "$dtb.analysis.txt"
done

# 4. Find the one with "kera" or "sm8750" and copy it
cp extracted_dtbs/dtb_XX.dtb \
    Platforms/KaanapaliPkg/Device/zte-np05j/DeviceTreeBlob/Android/android-np05j.dtb

# 5. Update display resolution in PcdsFixedAtBuild.dsc.inc based on analysis

# 6. Configure DXE files based on extracted binaries

# 7. Build
./build_uefi.py -d zte-np05j -t DEBUG
```

## Troubleshooting

### extract_uefi_binaries.py

**"No firmware volumes found!"**
- Image might be compressed or encrypted
- Try extracting from different partition (uefi_a vs uefi_b)
- Check if image needs decompression first

**Few binaries extracted**
- Normal for some devices with minimal UEFI implementations
- Compare with similar device to see if count is reasonable

### extract_dtb_from_dtbo.py

**"No DTBs found in image!"**
- Image might not be DTBO format
- Try `binwalk -e dtbo_a.img` as alternative
- Check if image is compressed

### analyze_dtb.py

**"Resolution not found in DTB"**
- Display info might use different property names
- Check raw DTS output for manual inspection
- May need to extract from different source (kernel config, etc.)

**"dtc not found"**
- Install: `sudo apt install device-tree-compiler`
- Script will still extract strings without dtc

## Additional Resources

- **SimpleGuide.md** - Complete porting guide
- **DefinesGuidance.md** - Configuration macros reference
- **UEFIReader** (original C# tool): https://github.com/WOA-Project/UEFIReader

## License

Same license as mu_aloha_platforms repository.
