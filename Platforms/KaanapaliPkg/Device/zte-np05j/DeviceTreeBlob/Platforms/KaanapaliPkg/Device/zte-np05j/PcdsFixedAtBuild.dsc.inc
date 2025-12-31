[PcdsFixedAtBuild.common]
# Display - PLACEHOLDER VALUES (need actual device specs)
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferWidth|1080
gAndromedaPkgTokenSpaceGuid.PcdMipiFrameBufferHeight|2400

# Display Caller
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerExitDisableDisplay|FALSE
#gAndromedaPkgTokenSpaceGuid.PcdDisplayCallerStallBeforeEnable|1000

# Smbios Info
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemBrand|"ZTE"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailSku|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemRetailModel|"ZTE PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosSystemModel|"PQ84P01"
gAndromedaPkgTokenSpaceGuid.PcdSmbiosBoardModel|"np05j"

# ABL Product name from device tree (kera)
gAndromedaPkgTokenSpaceGuid.PcdABLProduct|"kera"

[PcdsDynamicDefault.common]
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoHorizontalResolution|1080
gEfiMdeModulePkgTokenSpaceGuid.PcdVideoVerticalResolution|2400
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoHorizontalResolution|1080
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupVideoVerticalResolution|2400
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutColumn|135  # = 1080 / EFI_GLYPH_WIDTH(8)
gEfiMdeModulePkgTokenSpaceGuid.PcdSetupConOutRow|126     # = 2400 / EFI_GLYPH_HEIGHT(19)
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutColumn|135       # = 1080 / EFI_GLYPH_WIDTH(8)
gEfiMdeModulePkgTokenSpaceGuid.PcdConOutRow|126          # = 2400 / EFI_GLYPH_HEIGHT(19)
