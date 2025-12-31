# Placeholder for Android Device Tree Blob
# 
# REQUIRED: Copy your device's DTB here and name it: android-np05j.dtb
#
# How to get DTB:
# Option 1 - From running device:
#   adb shell su -c "cp /sys/firmware/fdt /sdcard/fdt"
#   adb pull /sdcard/fdt android-np05j.dtb
#
# Option 2 - Extract from boot.img using magiskboot:
#   magiskboot unpack boot.img
#   mv kernel_dtb android-np05j.dtb
#
# Option 3 - Use the dtbo_a.img from your firmware dump
#   (May need conversion/processing)

