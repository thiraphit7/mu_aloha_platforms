#!/usr/bin/env python3
"""
Enhanced UEFI Binary Extractor
Recursively extracts binaries from nested UEFI firmware volumes
Usage: python3 extract_uefi_binaries_enhanced.py <uefi_image> <output_dir>
"""

import sys
import os
import struct
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

class UEFIExtractorEnhanced:
    """Enhanced extractor with support for nested firmware volumes"""

    # File types
    FILE_TYPES = {
        0x00: 'UNKNOWN',
        0x01: 'RAW',
        0x02: 'FREEFORM',
        0x03: 'SECURITY_CORE',
        0x04: 'PEI_CORE',
        0x05: 'DXE_CORE',
        0x06: 'PEIM',
        0x07: 'DRIVER',
        0x08: 'COMBINED_PEIM_DRIVER',
        0x09: 'APPLICATION',
        0x0A: 'SMM',
        0x0B: 'FIRMWARE_VOLUME_IMAGE',
        0x0C: 'COMBINED_SMM_DXE',
        0x0D: 'SMM_CORE',
        0x0E: 'OEM_MIN',
        0x0F: 'DEBUG_MIN',
        0xF0: 'FFS_PAD',
    }

    # Section types
    SECTION_TYPES = {
        0x01: 'COMPRESSION',
        0x02: 'GUID_DEFINED',
        0x10: 'PE32',
        0x11: 'PIC',
        0x12: 'TE',
        0x13: 'DXE_DEPEX',
        0x14: 'VERSION',
        0x15: 'USER_INTERFACE',
        0x16: 'COMPATIBILITY16',
        0x17: 'FIRMWARE_VOLUME_IMAGE',
        0x18: 'FREEFORM_SUBTYPE_GUID',
        0x19: 'RAW',
        0x1B: 'PEI_DEPEX',
        0x1C: 'SMM_DEPEX',
    }

    def __init__(self, image_path: str, output_dir: str, verbose: bool = False):
        self.image_path = image_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.extracted_files = []
        self.processed_guids = set()  # Track processed GUIDs to avoid duplicates
        self.depth = 0  # Track recursion depth for logging

    def log(self, message: str, level: int = 0):
        """Print log message with indentation based on depth"""
        if self.verbose or level == 0:
            indent = "  " * self.depth
            print(f"{indent}{message}")

    def guid_to_str(self, guid_bytes: bytes) -> str:
        """Convert GUID bytes to string format"""
        if len(guid_bytes) != 16:
            return "INVALID_GUID"

        d1 = struct.unpack('<I', guid_bytes[0:4])[0]
        d2 = struct.unpack('<H', guid_bytes[4:6])[0]
        d3 = struct.unpack('<H', guid_bytes[6:8])[0]
        d4 = guid_bytes[8:10]
        d5 = guid_bytes[10:16]

        return f"{d1:08X}-{d2:04X}-{d3:04X}-{d4.hex().upper()}-{d5.hex().upper()}"

    def align(self, offset: int, alignment: int = 8) -> int:
        """Align offset to boundary"""
        return (offset + alignment - 1) & ~(alignment - 1)

    def find_firmware_volumes(self, data: bytes) -> List[int]:
        """Find all firmware volume headers in the image"""
        volumes = []
        signature = b'_FVH'
        offset = 0

        while offset < len(data):
            pos = data.find(signature, offset)
            if pos == -1:
                break
            # FV header signature is at offset 0x28
            fv_start = pos - 0x28
            if fv_start >= 0:
                volumes.append(fv_start)
            offset = pos + 1

        return volumes

    def extract_file(self, file_data: bytes, guid: str, file_type: int,
                    name: str = None, base_path: str = "") -> None:
        """Extract a single UEFI file and handle nested volumes"""
        type_name = self.FILE_TYPES.get(file_type, f'TYPE_{file_type:02X}')

        # Skip if already processed this GUID
        file_id = f"{guid}_{type_name}"
        if file_id in self.processed_guids:
            return
        self.processed_guids.add(file_id)

        # Parse sections
        offset = 0
        section_num = 0
        ui_name = name

        while offset < len(file_data):
            if offset + 4 > len(file_data):
                break

            # Read section header
            size_bytes = file_data[offset:offset+3]
            if len(size_bytes) < 3:
                break

            section_size = struct.unpack('<I', size_bytes + b'\x00')[0]
            if section_size == 0 or section_size == 0xFFFFFF:
                break

            section_type = file_data[offset+3] if offset+3 < len(file_data) else 0
            section_type_name = self.SECTION_TYPES.get(section_type, f'UNKNOWN_{section_type:02X}')

            # Handle different section types
            if section_type == 0x15:  # USER_INTERFACE
                # Extract UI name
                ui_data = file_data[offset+4:offset+section_size]
                try:
                    ui_name = ui_data.decode('utf-16le').rstrip('\x00')
                    ui_name = ui_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
                except:
                    pass

            elif section_type == 0x17:  # FIRMWARE_VOLUME_IMAGE (nested)
                self.log(f"Found nested FV in {guid}", 1)
                section_data = file_data[offset+4:offset+section_size]
                # Recursively process nested firmware volume
                self.depth += 1
                self.extract_from_nested_fv(section_data, guid)
                self.depth -= 1

            elif section_type in [0x10, 0x12, 0x19]:  # PE32, TE, RAW
                section_data = file_data[offset+4:offset+section_size]

                # Determine file extension
                ext = 'bin'
                if section_type == 0x10:  # PE32
                    ext = 'efi'
                elif section_type == 0x12:  # TE
                    ext = 'te'
                elif section_type == 0x19:  # RAW
                    ext = 'raw'

                # Build filename
                if ui_name:
                    filename = f"{ui_name}.{ext}"
                else:
                    filename = f"{guid}_{type_name}_{section_num:02d}.{ext}"

                # Create subdirectory structure for organization
                output_path = self.output_dir / base_path / filename
                output_path.parent.mkdir(parents=True, exist_ok=True)

                output_path.write_bytes(section_data)
                self.extracted_files.append(str(output_path))
                self.log(f"Extracted: {filename} ({section_type_name}, {len(section_data)} bytes)", 1)

                section_num += 1

            # Move to next section (aligned)
            offset = self.align(offset + section_size, 4)

    def parse_ffs_file(self, data: bytes, offset: int) -> Optional[Tuple]:
        """Parse a single FFS file header"""
        if offset + 24 > len(data):
            return None

        header = data[offset:offset+24]

        # Check for padding or erased file
        if header == b'\xff' * 24:
            return None

        # Parse header
        guid = header[0:16]
        checksum = header[16:18]
        file_type = header[18]
        attributes = header[19]
        size_bytes = header[20:23]
        state = header[23]

        # Calculate size
        file_size = struct.unpack('<I', size_bytes + b'\x00')[0]

        if file_size == 0 or file_size == 0xFFFFFF:
            return None

        return (guid, file_type, file_size, offset + 24)

    def extract_from_nested_fv(self, fv_data: bytes, parent_guid: str = ""):
        """Extract files from a nested firmware volume"""
        self.log(f"Processing nested FV (size: {len(fv_data)} bytes)", 1)

        # Try to find FV header signature
        fv_header_sig = b'_FVH'
        sig_pos = fv_data.find(fv_header_sig)

        if sig_pos == -1:
            # No FV header, try parsing as raw FFS
            file_offset = 0
        else:
            # Skip FV header
            file_offset = sig_pos - 0x28 + 56  # FV header minimum size

        # Align to 8 bytes
        file_offset = self.align(file_offset, 8)

        # Parse files
        while file_offset < len(fv_data):
            result = self.parse_ffs_file(fv_data, file_offset)
            if result is None:
                file_offset = self.align(file_offset + 8, 8)
                continue

            guid, file_type, file_size, data_offset = result
            guid_str = self.guid_to_str(guid)
            type_name = self.FILE_TYPES.get(file_type, f'TYPE_{file_type:02X}')

            self.log(f"Nested file: {guid_str} (Type: {type_name}, Size: {file_size})", 2)

            # Extract file data
            file_data = fv_data[data_offset:data_offset + file_size - 24]

            if file_type not in [0xF0, 0x00]:  # Skip PAD and UNKNOWN
                # Create subdirectory for nested files
                base_path = f"nested_{parent_guid[:8]}" if parent_guid else "nested"
                self.extract_file(file_data, guid_str, file_type, base_path=base_path)

            # Move to next file (aligned)
            file_offset = self.align(file_offset + file_size, 8)

    def extract_from_volume(self, data: bytes, volume_offset: int, volume_num: int = 0) -> None:
        """Extract all files from a firmware volume"""
        self.log(f"\nProcessing firmware volume #{volume_num} at offset 0x{volume_offset:X}")

        # Skip FV header (minimum 56 bytes)
        file_offset = volume_offset + 56

        # Align to 8 bytes
        file_offset = self.align(file_offset, 8)

        while file_offset < len(data):
            result = self.parse_ffs_file(data, file_offset)
            if result is None:
                file_offset = self.align(file_offset + 8, 8)
                continue

            guid, file_type, file_size, data_offset = result
            guid_str = self.guid_to_str(guid)
            type_name = self.FILE_TYPES.get(file_type, f'TYPE_{file_type:02X}')

            self.log(f"Found file: {guid_str} (Type: {type_name}, Size: {file_size})")

            # Extract file data
            file_data = data[data_offset:data_offset + file_size - 24]

            # Handle FIRMWARE_VOLUME_IMAGE specially
            if file_type == 0x0B:  # FIRMWARE_VOLUME_IMAGE
                self.log("  → This is a nested firmware volume, processing recursively...")
                self.depth += 1
                self.extract_file(file_data, guid_str, file_type)
                self.depth -= 1
            elif file_type not in [0xF0, 0x00]:  # Skip PAD and UNKNOWN
                self.extract_file(file_data, guid_str, file_type)

            # Move to next file (aligned)
            file_offset = self.align(file_offset + file_size, 8)

    def extract(self) -> int:
        """Main extraction function"""
        self.log(f"Reading UEFI image: {self.image_path}")

        try:
            with open(self.image_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1

        self.log(f"Image size: {len(data)} bytes")

        # Find firmware volumes
        volumes = self.find_firmware_volumes(data)

        if not volumes:
            self.log("No firmware volumes found!")
            self.log("Trying to parse as raw FFS...")
            # Try parsing from beginning
            self.extract_from_volume(data, 0, 0)
        else:
            self.log(f"Found {len(volumes)} firmware volume(s)")
            for i, vol_offset in enumerate(volumes):
                self.extract_from_volume(data, vol_offset, i)

        self.log(f"\nExtraction complete!")
        self.log(f"Extracted {len(self.extracted_files)} file(s) to {self.output_dir}")

        # Print summary by file type
        efi_count = sum(1 for f in self.extracted_files if f.endswith('.efi'))
        te_count = sum(1 for f in self.extracted_files if f.endswith('.te'))
        raw_count = sum(1 for f in self.extracted_files if f.endswith('.raw'))

        self.log(f"\nFile type summary:")
        self.log(f"  .efi files: {efi_count}")
        self.log(f"  .te files: {te_count}")
        self.log(f"  .raw files: {raw_count}")

        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Enhanced UEFI binary extractor with nested volume support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s uefi_a.img output_binaries/
  %(prog)s firmware.bin Binaries/ -v
        '''
    )

    parser.add_argument('image', help='UEFI firmware image file')
    parser.add_argument('output', help='Output directory for extracted binaries')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: Input file '{args.image}' not found!")
        return 1

    extractor = UEFIExtractorEnhanced(args.image, args.output, args.verbose)
    return extractor.extract()


if __name__ == '__main__':
    sys.exit(main())
