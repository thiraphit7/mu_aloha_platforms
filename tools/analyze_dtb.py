#!/usr/bin/env python3
"""
DTB Analyzer
Analyzes Device Tree Blob files to extract hardware information
Usage: python3 analyze_dtb.py <dtb_file>
"""

import sys
import os
import struct
import subprocess
from pathlib import Path
import argparse
import re

class DTBAnalyzer:
    """Analyze DTB files for hardware information"""

    DTB_MAGIC = 0xD00DFEED

    def __init__(self, dtb_path: str):
        self.dtb_path = dtb_path
        self.dts_content = None

    def read_u32_be(self, data: bytes, offset: int) -> int:
        """Read big-endian uint32"""
        return struct.unpack('>I', data[offset:offset+4])[0]

    def verify_dtb(self) -> bool:
        """Verify DTB magic number"""
        try:
            with open(self.dtb_path, 'rb') as f:
                magic = self.read_u32_be(f.read(4), 0)
                return magic == self.DTB_MAGIC
        except:
            return False

    def decompile_dtb(self) -> bool:
        """Decompile DTB to DTS using dtc"""
        try:
            result = subprocess.run(
                ['dtc', '-I', 'dtb', '-O', 'dts', self.dtb_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.dts_content = result.stdout
                return True
            else:
                print(f"dtc error: {result.stderr}")
                return False

        except FileNotFoundError:
            print("Warning: 'dtc' (device tree compiler) not found")
            print("Install with: sudo apt install device-tree-compiler")
            return False
        except subprocess.TimeoutExpired:
            print("Timeout while decompiling DTB")
            return False
        except Exception as e:
            print(f"Error decompiling DTB: {e}")
            return False

    def extract_strings(self) -> list:
        """Extract printable strings from DTB"""
        try:
            with open(self.dtb_path, 'rb') as f:
                data = f.read()

            strings = []
            current = []

            for byte in data:
                if 32 <= byte <= 126:  # Printable ASCII
                    current.append(chr(byte))
                elif byte == 0 and len(current) >= 4:
                    strings.append(''.join(current))
                    current = []
                else:
                    current = []

            return strings

        except Exception as e:
            print(f"Error extracting strings: {e}")
            return []

    def find_display_info(self) -> dict:
        """Find display resolution and panel information"""
        info = {
            'resolution': None,
            'width': None,
            'height': None,
            'panel': None,
            'compatible': []
        }

        if not self.dts_content:
            return info

        # Look for display panel nodes
        panel_patterns = [
            r'panel[@-].*?{',
            r'display[@-].*?{',
            r'framebuffer[@-].*?{',
            r'mdss_dsi.*?{',
        ]

        for pattern in panel_patterns:
            matches = re.finditer(pattern, self.dts_content, re.MULTILINE)
            for match in matches:
                # Extract the section
                start = match.start()
                # Find matching closing brace
                depth = 0
                end = start
                for i in range(start, len(self.dts_content)):
                    if self.dts_content[i] == '{':
                        depth += 1
                    elif self.dts_content[i] == '}':
                        depth -= 1
                        if depth == 0:
                            end = i
                            break

                section = self.dts_content[start:end+1]

                # Look for resolution
                res_match = re.search(r'qcom,mdss-dsi-panel-width\s*=\s*<0x([0-9a-fA-F]+)>', section)
                if res_match:
                    info['width'] = int(res_match.group(1), 16)

                res_match = re.search(r'qcom,mdss-dsi-panel-height\s*=\s*<0x([0-9a-fA-F]+)>', section)
                if res_match:
                    info['height'] = int(res_match.group(1), 16)

                # Alternative patterns
                res_match = re.search(r'width\s*=\s*<0x([0-9a-fA-F]+)>', section)
                if res_match and not info['width']:
                    info['width'] = int(res_match.group(1), 16)

                res_match = re.search(r'height\s*=\s*<0x([0-9a-fA-F]+)>', section)
                if res_match and not info['height']:
                    info['height'] = int(res_match.group(1), 16)

                # Panel name/compatible
                comp_match = re.search(r'compatible\s*=\s*"([^"]+)"', section)
                if comp_match:
                    info['compatible'].append(comp_match.group(1))

        # Try to find resolution from other patterns
        if not info['width']:
            patterns = [
                r'hactive\s*=\s*<0x([0-9a-fA-F]+)>',
                r'xres\s*=\s*<0x([0-9a-fA-F]+)>',
                r'horizontal-resolution\s*=\s*<0x([0-9a-fA-F]+)>',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.dts_content)
                if match:
                    info['width'] = int(match.group(1), 16)
                    break

        if not info['height']:
            patterns = [
                r'vactive\s*=\s*<0x([0-9a-fA-F]+)>',
                r'yres\s*=\s*<0x([0-9a-fA-F]+)>',
                r'vertical-resolution\s*=\s*<0x([0-9a-fA-F]+)>',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.dts_content)
                if match:
                    info['height'] = int(match.group(1), 16)
                    break

        if info['width'] and info['height']:
            info['resolution'] = f"{info['width']}x{info['height']}"

        return info

    def find_memory_info(self) -> dict:
        """Find memory configuration"""
        info = {
            'total': None,
            'regions': []
        }

        if not self.dts_content:
            return info

        # Look for memory nodes
        memory_pattern = r'memory[@]([0-9a-fA-F]+)\s*{[^}]*reg\s*=\s*<0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)>'

        matches = re.finditer(memory_pattern, self.dts_content, re.MULTILINE)
        total_memory = 0

        for match in matches:
            addr_hi = int(match.group(2), 16)
            addr_lo = int(match.group(3), 16)
            size_hi = int(match.group(4), 16)
            size_lo = int(match.group(5), 16)

            address = (addr_hi << 32) | addr_lo
            size = (size_hi << 32) | size_lo

            info['regions'].append({
                'address': f"0x{address:X}",
                'size': size,
                'size_mb': size // (1024 * 1024)
            })

            total_memory += size

        if total_memory > 0:
            info['total'] = total_memory
            info['total_gb'] = total_memory / (1024 * 1024 * 1024)

        return info

    def find_soc_info(self) -> dict:
        """Find SoC information"""
        info = {
            'compatible': [],
            'model': None,
            'soc': None
        }

        if not self.dts_content:
            return info

        # Root compatible
        root_match = re.search(r'^\s*compatible\s*=\s*"([^"]+)"', self.dts_content, re.MULTILINE)
        if root_match:
            info['compatible'] = root_match.group(1).split(',')

        # Model
        model_match = re.search(r'^\s*model\s*=\s*"([^"]+)"', self.dts_content, re.MULTILINE)
        if model_match:
            info['model'] = model_match.group(1)

        # SoC node
        soc_match = re.search(r'soc[@-].*?{[^}]*compatible\s*=\s*"([^"]+)"', self.dts_content, re.MULTILINE)
        if soc_match:
            info['soc'] = soc_match.group(1)

        return info

    def analyze(self) -> int:
        """Main analysis function"""
        print(f"{'='*60}")
        print(f"DTB Analysis: {Path(self.dtb_path).name}")
        print(f"{'='*60}\n")

        # Verify DTB
        if not self.verify_dtb():
            print("Error: Invalid DTB file (bad magic number)")
            return 1

        print("✓ Valid DTB file\n")

        # Try to decompile
        print("Attempting to decompile DTB...")
        if self.decompile_dtb():
            print("✓ Successfully decompiled\n")

            # Extract information
            print("-" * 60)
            print("SOC INFORMATION")
            print("-" * 60)
            soc_info = self.find_soc_info()
            if soc_info['model']:
                print(f"Model: {soc_info['model']}")
            if soc_info['soc']:
                print(f"SoC: {soc_info['soc']}")
            if soc_info['compatible']:
                print(f"Compatible: {', '.join(soc_info['compatible'])}")

            print("\n" + "-" * 60)
            print("DISPLAY INFORMATION")
            print("-" * 60)
            display_info = self.find_display_info()
            if display_info['resolution']:
                print(f"✓ Resolution: {display_info['resolution']}")
                print(f"  Width: {display_info['width']}")
                print(f"  Height: {display_info['height']}")
            else:
                print("× Resolution not found in DTB")

            if display_info['compatible']:
                print(f"Panel Compatible:")
                for comp in display_info['compatible']:
                    print(f"  - {comp}")

            print("\n" + "-" * 60)
            print("MEMORY INFORMATION")
            print("-" * 60)
            memory_info = self.find_memory_info()
            if memory_info['total']:
                print(f"✓ Total Memory: {memory_info['total_gb']:.2f} GB ({memory_info['total']} bytes)")
                print(f"Memory Regions: {len(memory_info['regions'])}")
                for i, region in enumerate(memory_info['regions']):
                    print(f"  Region {i}: {region['address']} - {region['size_mb']} MB")
            else:
                print("× Memory information not found")

        else:
            print("✗ Could not decompile DTB\n")
            print("Extracting strings instead...\n")

            strings = self.extract_strings()

            # Filter for interesting strings
            interesting = []
            keywords = ['panel', 'display', 'resolution', 'qcom', 'kera', 'sm8750',
                       'width', 'height', 'compatible', 'model', 'manufacturer']

            for s in strings:
                lower = s.lower()
                if any(kw in lower for kw in keywords):
                    interesting.append(s)

            print("Interesting strings found:")
            for s in sorted(set(interesting)):
                print(f"  {s}")

        print(f"\n{'='*60}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Analyze DTB (Device Tree Blob) files for hardware information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s dtb_00.dtb
  %(prog)s android-np05j.dtb
        '''
    )

    parser.add_argument('dtb', help='DTB file to analyze')

    args = parser.parse_args()

    if not os.path.exists(args.dtb):
        print(f"Error: DTB file '{args.dtb}' not found!")
        return 1

    analyzer = DTBAnalyzer(args.dtb)
    return analyzer.analyze()


if __name__ == '__main__':
    sys.exit(main())
