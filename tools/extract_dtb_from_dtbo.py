#!/usr/bin/env python3
"""
DTB Extractor from DTBO
Extracts Device Tree Blobs from DTBO (Device Tree Blob Overlay) images
Usage: python3 extract_dtb_from_dtbo.py <dtbo_image> <output_dir>
"""

import sys
import os
import struct
from pathlib import Path
import argparse

class DTBOExtractor:
    """Extract DTBs from Android DTBO images"""

    # DTBO magic number
    DTBO_MAGIC = 0xD7B7AB1E

    # DTB magic number
    DTB_MAGIC = 0xD00DFEED

    def __init__(self, dtbo_path: str, output_dir: str):
        self.dtbo_path = dtbo_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_dtbs = []

    def read_u32_be(self, data: bytes, offset: int) -> int:
        """Read big-endian uint32"""
        return struct.unpack('>I', data[offset:offset+4])[0]

    def read_u32_le(self, data: bytes, offset: int) -> int:
        """Read little-endian uint32"""
        return struct.unpack('<I', data[offset:offset+4])[0]

    def find_dtb_magic(self, data: bytes, start: int = 0) -> list:
        """Find all DTB magic numbers in data"""
        positions = []
        offset = start

        while offset < len(data) - 4:
            pos = data.find(struct.pack('>I', self.DTB_MAGIC), offset)
            if pos == -1:
                break
            positions.append(pos)
            offset = pos + 4

        return positions

    def extract_dtbo_format(self, data: bytes) -> bool:
        """Extract DTBs from Android DTBO format"""
        if len(data) < 32:
            return False

        # Check DTBO magic
        magic = self.read_u32_be(data, 0)
        if magic != self.DTBO_MAGIC:
            return False

        print("Detected Android DTBO format")

        # Parse DTBO header
        total_size = self.read_u32_be(data, 4)
        header_size = self.read_u32_be(data, 8)
        dt_entry_size = self.read_u32_be(data, 12)
        dt_entry_count = self.read_u32_be(data, 16)
        dt_entries_offset = self.read_u32_be(data, 20)
        page_size = self.read_u32_be(data, 24)
        version = self.read_u32_be(data, 28)

        print(f"DTBO Header:")
        print(f"  Total size: {total_size}")
        print(f"  Header size: {header_size}")
        print(f"  Entry size: {dt_entry_size}")
        print(f"  Entry count: {dt_entry_count}")
        print(f"  Entries offset: 0x{dt_entries_offset:X}")
        print(f"  Page size: {page_size}")
        print(f"  Version: {version}")

        # Extract each DTB
        for i in range(dt_entry_count):
            entry_offset = dt_entries_offset + (i * dt_entry_size)

            if entry_offset + dt_entry_size > len(data):
                break

            # Read DT entry (32 bytes for version 0, may vary for other versions)
            dt_size = self.read_u32_be(data, entry_offset)
            dt_offset = self.read_u32_be(data, entry_offset + 4)

            print(f"\nDTB Entry {i}:")
            print(f"  Offset: 0x{dt_offset:X}")
            print(f"  Size: {dt_size} bytes")

            if dt_offset + dt_size > len(data):
                print(f"  Warning: DTB extends beyond file!")
                continue

            # Extract DTB
            dtb_data = data[dt_offset:dt_offset + dt_size]

            # Verify DTB magic
            dtb_magic = self.read_u32_be(dtb_data, 0)
            if dtb_magic != self.DTB_MAGIC:
                print(f"  Warning: Invalid DTB magic: 0x{dtb_magic:08X}")
                continue

            # Save DTB
            output_file = self.output_dir / f"dtb_{i:02d}.dtb"
            output_file.write_bytes(dtb_data)
            self.extracted_dtbs.append(str(output_file))
            print(f"  Extracted to: {output_file.name}")

        return dt_entry_count > 0

    def extract_raw_dtbs(self, data: bytes) -> bool:
        """Extract DTBs from raw concatenated format"""
        print("Searching for DTB magic numbers...")

        dtb_positions = self.find_dtb_magic(data)

        if not dtb_positions:
            return False

        print(f"Found {len(dtb_positions)} potential DTB(s)")

        for i, pos in enumerate(dtb_positions):
            # Determine size
            if i + 1 < len(dtb_positions):
                dtb_size = dtb_positions[i + 1] - pos
            else:
                # For last DTB, try to read size from header
                if pos + 8 <= len(data):
                    dtb_size = self.read_u32_be(data, pos + 4)
                    if dtb_size == 0 or dtb_size > len(data) - pos:
                        dtb_size = len(data) - pos
                else:
                    dtb_size = len(data) - pos

            print(f"\nDTB {i}:")
            print(f"  Offset: 0x{pos:X}")
            print(f"  Size: {dtb_size} bytes")

            # Extract DTB
            dtb_data = data[pos:pos + dtb_size]

            # Save DTB
            output_file = self.output_dir / f"dtb_{i:02d}.dtb"
            output_file.write_bytes(dtb_data)
            self.extracted_dtbs.append(str(output_file))
            print(f"  Extracted to: {output_file.name}")

        return len(dtb_positions) > 0

    def extract(self) -> int:
        """Main extraction function"""
        print(f"Reading DTBO/DTB image: {self.dtbo_path}")

        try:
            with open(self.dtbo_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1

        print(f"Image size: {len(data)} bytes\n")

        # Try Android DTBO format first
        if not self.extract_dtbo_format(data):
            # Try raw DTB concatenation
            if not self.extract_raw_dtbs(data):
                print("No DTBs found in image!")
                return 1

        print(f"\n{'='*60}")
        print(f"Extraction complete!")
        print(f"Extracted {len(self.extracted_dtbs)} DTB(s) to {self.output_dir}")

        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Extract DTB files from DTBO (Device Tree Blob Overlay) images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s dtbo_a.img extracted_dtbs/
  %(prog)s dtbo.img DeviceTreeBlob/Android/
        '''
    )

    parser.add_argument('image', help='DTBO image file')
    parser.add_argument('output', help='Output directory for extracted DTB files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: Input file '{args.image}' not found!")
        return 1

    extractor = DTBOExtractor(args.image, args.output)
    return extractor.extract()


if __name__ == '__main__':
    sys.exit(main())
