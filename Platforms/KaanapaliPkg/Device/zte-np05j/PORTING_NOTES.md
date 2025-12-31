# ZTE np05j Porting Notes

## Porting Strategy

This device port uses a simpler approach than creating a completely new platform:

- **Silicon**: Uses existing `Silicon/QC/Sm8850/` (not creating new SM8750 package)
- **Platform Package**: Uses existing `Platforms/KaanapaliPkg/`
- **Device Template**: Based on `oneplus-plk110`
- **Target**: `Platforms/KaanapaliPkg/Device/zte-np05j/`

## Rationale

While the source firmware is built for SM8750 (Pakala/Kera platform), we're using SM8850 as the base because:

1. **SM8850 is the closest available** - Most similar architecture
2. **Reduces complexity** - No need to create new silicon package
3. **Faster iteration** - Can leverage existing working code
4. **Easier maintenance** - Fewer moving parts

When official SM8750 support becomes available or if we encounter SM8750-specific issues, we can migrate to a dedicated SM8750 silicon package.

## Changes Made

### 1. Device Configuration

**File**: `PcdsFixedAtBuild.dsc.inc`

Updated device information:
- Brand: "ZTE"
- Model: "PQ84P01"
- Board: "np05j"
- ABL Product: "kera" (from device tree)
- Display: 1080x2400 (placeholder, needs verification)

### 2. Device Tree

**File**: `DeviceTreeBlob/dtbo_a.img`

Copied from source firmware:
- Platform: qcom,kera-rumi
- Size: 25MB (DTBO overlay format)

### 3. Libraries

Currently using oneplus-plk110 libraries as-is:
- `PlatformMemoryMapLib` - May need adjustment for device-specific memory layout
- `PlatformConfigurationMapLib` - May need GPIO/peripheral updates

## Known Limitations

### Using SM8850 Instead of SM8750

**Potential Issues:**
- Memory map differences
- Peripheral base addresses may differ
- Clock configurations might not match
- Some hardware features may not work correctly

**Mitigation:**
- Test thoroughly
- Update memory maps as needed
- Document any SM8850-specific workarounds
- Be ready to migrate to SM8750 if needed

### RUMI Firmware Source

The source firmware is from RUMI (pre-silicon emulation):
- May have differences from actual silicon
- Some configurations might be emulation-specific
- Need real device specs for accurate configuration

### Placeholder Values

**Display Resolution**: Currently 1080x2400
- **Status**: Placeholder
- **Action Needed**: Verify from device specifications
- **Impact**: Display may not render correctly if wrong

**Memory Configuration**: Using plk110 memory map
- **Status**: Needs verification
- **Action Needed**: Extract from DTBO or device specs
- **Impact**: May cause boot failures or stability issues

## Next Steps

### Immediate
1. ✅ Create device directory structure
2. ✅ Copy and adapt configuration files
3. ✅ Update device-specific PCDs
4. ⏳ Initialize build environment
5. ⏳ Attempt first build

### Testing & Validation
1. Verify build completes successfully
2. Analyze generated firmware image
3. Test boot on device (if available)
4. Verify display initialization
5. Check storage and USB functionality

### Optimization
1. Extract actual device specs from DTBO
2. Update display resolution if different
3. Optimize memory map for this device
4. Update GPIO mappings for buttons
5. Fine-tune device configuration

### Future Enhancements
1. Add ACPI/DSDT support
2. Improve hardware compatibility
3. Add device-specific features
4. Consider SM8750 silicon package if needed

## Testing Checklist

### Build Phase
- [ ] Build environment initialized
- [ ] Compilation succeeds without errors
- [ ] Firmware image generated
- [ ] Image format verified (Android boot image)

### Boot Phase (if device available)
- [ ] Device powers on
- [ ] UEFI firmware loads
- [ ] Display shows output
- [ ] UEFI menu appears
- [ ] Can navigate with buttons

### Hardware Phase
- [ ] Storage (UFS) detected
- [ ] USB functioning
- [ ] Power management working
- [ ] Buttons responding correctly

### OS Boot Phase
- [ ] Can boot Windows
- [ ] Can boot Linux
- [ ] All hardware working in OS
- [ ] Stable operation

## Reference Files

### Source Firmware
- Path: `/home/zte/workspace/PQ84P01_NON_EEA_V_SM8750_TARGET_V_TA_20250430_03_DAILYBUILD/`
- Bootloader: BOOT.MXF.2.5.1
- Platform: PakalaLAA
- Build Date: 2025-04-30

### Base Template
- Silicon: `Silicon/QC/Sm8850/`
- Platform: `Platforms/KaanapaliPkg/`
- Device: `Platforms/KaanapaliPkg/Device/oneplus-plk110/`

### Documentation
- Analysis: `np05j/ANALYSIS.md`
- Detailed Plan: `np05j/PORTING_PLAN.md`
- Summary: `np05j/SUMMARY.md`

## Troubleshooting

### Build Errors

**Problem**: Missing QcomPkg.dsc.inc
- **Cause**: SM8850 silicon package incomplete
- **Solution**: Ensure Silicon/QC/Sm8850/ is properly structured

**Problem**: Binary files not found
- **Cause**: Binaries may be SM8850-specific
- **Solution**: Adjust DXE.inc to skip missing binaries or find SM8750 equivalents

**Problem**: Memory map errors
- **Cause**: Device-specific memory layout differs
- **Solution**: Update PlatformMemoryMapLib with correct memory regions

### Runtime Errors

**Problem**: Black screen
- **Cause**: Display initialization failed
- **Solutions**:
  - Verify display resolution is correct
  - Check SimpleFbDxe configuration
  - Review DTBO for panel configuration

**Problem**: Boot hangs
- **Cause**: Memory map or peripheral address mismatch
- **Solutions**:
  - Review memory configuration
  - Check for SM8750-specific addresses
  - Enable DEBUG output for diagnostics

**Problem**: Immediate reboot
- **Cause**: Critical initialization failure
- **Solutions**:
  - Check APRIORI driver load order
  - Verify required binaries are present
  - Review early boot configuration

## Migration to SM8750 (Future)

If/when we need to migrate to proper SM8750 support:

### Create SM8750 Silicon Package
1. Copy `Silicon/QC/Sm8850/` to `Silicon/QC/Sm8750/`
2. Update GUIDs in QcomPkg.dec
3. Update memory maps and addresses
4. Update peripheral configurations

### Update Build Configuration
1. Create `build_cfg/sm8750.json`
2. Update platform references
3. Test build with new silicon package

### Migrate Device Configuration
1. Move to new KeraPkg if needed
2. Update DSC/FDF references
3. Adjust for SM8750-specific features

## Contact & Support

For questions or issues:
- Review documentation in `np05j/` directory
- Check reference platform: KaanapaliPkg/oneplus-plk110
- Consult mu_aloha_platforms community
