#!/bin/bash
# Script to analyze DTBO image and extract useful information

set -e

DTBO_FILE="np05j/dtbo_a.img"
OUTPUT_DIR="np05j/dtbo_analysis"

echo "=== DTBO Analysis Script ==="
echo ""

# Check if DTBO exists
if [ ! -f "$DTBO_FILE" ]; then
    echo "Error: $DTBO_FILE not found!"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Analyzing $DTBO_FILE..."
echo ""

#==============================================================================
# Basic file information
#==============================================================================
echo "1. File Information:"
echo "-------------------"
ls -lh "$DTBO_FILE"
file "$DTBO_FILE"
echo ""

#==============================================================================
# Try to extract with dtc
#==============================================================================
echo "2. Attempting to extract Device Tree Source:"
echo "--------------------------------------------"

if command -v dtc &> /dev/null; then
    echo "dtc is available, attempting extraction..."

    # Try direct decompilation
    if dtc -I dtb -O dts -o "$OUTPUT_DIR/dtbo.dts" "$DTBO_FILE" 2>"$OUTPUT_DIR/dtc_errors.log"; then
        echo "✓ Successfully extracted to $OUTPUT_DIR/dtbo.dts"
        echo ""
        echo "Device Tree Summary:"
        echo "-------------------"

        # Extract useful info
        echo "Compatible strings:"
        grep "compatible" "$OUTPUT_DIR/dtbo.dts" | head -20 || echo "  (none found)"
        echo ""

        echo "Model information:"
        grep "model" "$OUTPUT_DIR/dtbo.dts" | head -10 || echo "  (none found)"
        echo ""

        echo "Memory nodes:"
        grep -A 2 "memory@" "$OUTPUT_DIR/dtbo.dts" | head -20 || echo "  (none found)"
        echo ""
    else
        echo "⚠ Direct extraction failed. DTBO may need special handling."
        echo "  Error log saved to $OUTPUT_DIR/dtc_errors.log"

        # DTBO images might be in overlay format
        echo ""
        echo "Note: This appears to be a DTBO (Device Tree Blob Overlay) image."
        echo "      These are applied on top of a base DTB and may not decompile directly."
    fi
else
    echo "⚠ dtc (Device Tree Compiler) not installed."
    echo "  Install with: sudo apt-get install device-tree-compiler"
fi

echo ""

#==============================================================================
# Extract strings
#==============================================================================
echo "3. Extracting strings from DTBO:"
echo "--------------------------------"

strings "$DTBO_FILE" > "$OUTPUT_DIR/dtbo_strings.txt"
echo "✓ Strings saved to $OUTPUT_DIR/dtbo_strings.txt"
echo ""

# Show interesting strings
echo "Platform identifiers found:"
strings "$DTBO_FILE" | grep -iE "qcom|kera|pakala|sm8750|zte" | sort -u || echo "  (none found)"
echo ""

echo "Compatible device strings:"
strings "$DTBO_FILE" | grep "compatible" | head -10 || echo "  (none found)"
echo ""

echo "Memory-related strings:"
strings "$DTBO_FILE" | grep -iE "memory|ram|ddr" | head -10 || echo "  (none found)"
echo ""

#==============================================================================
# Hex dump analysis
#==============================================================================
echo "4. Creating hex dump (first 1KB):"
echo "----------------------------------"

if command -v xxd &> /dev/null; then
    xxd "$DTBO_FILE" | head -64 > "$OUTPUT_DIR/dtbo_hexdump_header.txt"
    echo "✓ Hex dump saved to $OUTPUT_DIR/dtbo_hexdump_header.txt"
else
    od -A x -t x1z -v "$DTBO_FILE" | head -64 > "$OUTPUT_DIR/dtbo_hexdump_header.txt"
    echo "✓ Hex dump saved to $OUTPUT_DIR/dtbo_hexdump_header.txt"
fi

# Show header
echo ""
echo "File header (first 64 bytes):"
head -4 "$OUTPUT_DIR/dtbo_hexdump_header.txt"
echo ""

#==============================================================================
# Check for Device Tree magic
#==============================================================================
echo "5. Checking for Device Tree markers:"
echo "------------------------------------"

# DTB magic is 0xd00dfeed
MAGIC=$(od -An -t x4 -N 4 "$DTBO_FILE" | tr -d ' ')
echo "First 4 bytes (magic): 0x$MAGIC"

if [ "$MAGIC" == "d00dfeed" ] || [ "$MAGIC" == "edfe0dd0" ]; then
    echo "✓ Valid Device Tree Blob magic found!"
else
    echo "⚠ Unexpected magic. This may not be a standard DTB."
    echo "  Could be Android DTBO format with additional headers."
fi

echo ""

#==============================================================================
# Look for Android DTBO header
#==============================================================================
echo "6. Checking for Android DTBO format:"
echo "------------------------------------"

# Android DTBO has "DTBO" magic at start
HEAD_MAGIC=$(dd if="$DTBO_FILE" bs=1 count=4 2>/dev/null | od -An -tx1 | tr -d ' ')
echo "Header magic: 0x$HEAD_MAGIC"

if echo "$HEAD_MAGIC" | grep -q "44544f42"; then  # "DTBO" in hex
    echo "✓ Android DTBO format detected!"
    echo ""
    echo "Note: Android DTBO images contain multiple DT overlays."
    echo "      May need special tools to extract individual overlays."
else
    echo "No Android DTBO header found."
fi

echo ""

#==============================================================================
# Summary
#==============================================================================
echo "=== Analysis Complete ==="
echo ""
echo "Output files created in $OUTPUT_DIR/:"
ls -1 "$OUTPUT_DIR/"
echo ""
echo "Key findings:"
echo "-------------"
echo "Platform: $(strings "$DTBO_FILE" | grep -o "qcom,kera[^\"]*" | head -1 || echo "unknown")"
echo "Size: $(ls -lh "$DTBO_FILE" | awk '{print $5}')"
echo ""
echo "Next steps:"
echo "1. Review $OUTPUT_DIR/dtbo.dts (if extracted)"
echo "2. Check $OUTPUT_DIR/dtbo_strings.txt for device information"
echo "3. Look for memory configuration, display info, GPIO mappings"
echo ""
