# DXE Phase Configuration for ZTE PQ84P01 (np05j)
# Based on oneplus-plk110 structure, adapted for Pakala (SM8750) platform

FILE FREEFORM = DDE58710-41CD-4306-DBFB-3FA90BB1D2DD {
    SECTION UI = "uefiplat.cfg"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/uefiplat.cfg
}

# AndromedaPkg Drivers
INF AndromedaPkg/Driver/SimpleFbDxe/SimpleFbDxe.inf
INF AndromedaPkg/Driver/RamPartitionDxe/RamPartitionDxe.inf

# Core QcomPkg Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/EnvDxe/EnvDxeEnhanced.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ParserDxe/ParserEnhancedDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PsStateDxe/PsStateDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/VariableDxe/VariableDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/EmbeddedMonotonicCounter/EmbeddedMonotonicCounter.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ResetRuntimeDxe/ResetRuntimeDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/VendorLogfsDxe/VendorLogfsDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/CfgUtilDxe/CfgUtilDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/FontDxe/FontDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QcomWDogDxe/QcomWDogDxe.inf

# Platform Information Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ChipInfoDxe/ChipInfoDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PlatformInfoDxe/PlatformInfoDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/DALSYSDxe/DALSYSDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/HALIOMMUDxe/HALIOMMUDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/HWIODxe/HWIODxe.inf

# I/O Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/I2CDxe/I2CDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/TLMMDxe/TLMMDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QupDxe/QupDxe.inf

# Power Management Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/CmdDbDxe/CmdDbDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PwrUtilsDxe/PwrUtilsDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/RpmhDxe/RpmhDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/NpaDxe/NpaDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ULogDxe/ULogDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/VcsDxe/VcsDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ClockDxe/ClockDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/CPRDxe/CPRDxe.inf

# System Resources
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ICBDxe/ICBDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SmemDxe/SmemDxe.inf

# Communication Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/MailboxDxe/MailboxDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QcomScmiDxe/QcomScmiDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/IPCCDxe/IPCCDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/GLinkDxe/GLinkDxe.inf

# Peripheral Drivers
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ButtonsDxe/ButtonsDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/GpiDxe/GpiDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SPMIDxe/SPMIDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/CalibrationDxe/CalibrationDxe.inf

# Security & Trust Zone
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/TzDxe/ScmDxeCompat.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/TzDxe/TzDxeLA.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ShmBridgeDxe/ShmBridgeDxeLA.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/VerifiedBootDxe/VerifiedBootDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QRKSDxe/QRKSDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/RNGDxe/RngDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SecRSADxe/SecRSADxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ASN1X509Dxe/ASN1X509Dxe.inf

# Storage Drivers
FILE DRIVER = 6b38f7b4-ad98-40e9-9093-aca2b5a253c4 {
    SECTION PE32 = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/MdeModulePkg/Universal/Disk/DiskIoDxe/DiskIoDxe.efi
    SECTION UI = "DiskIoDxe"
}

FILE DRIVER = 1fa1f39e-feff-4aae-bd7b-38a070a3b609 {
    SECTION PE32 = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/MdeModulePkg/Universal/Disk/PartitionDxe/PartitionDxe.efi
    SECTION UI = "PartitionDxe"
}

INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UFSDxe/UFSDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SdccDxe/SdccDxe.inf

# Resource Management
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SPSSDxe/SPSSDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/RmVmDxe/RmVmDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/RscDxe/RscDxe.inf

# BDS and Applications
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QcomBds/QcomBds.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Application/QcomChargerApp/QcomChargerApp.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Application/Ebl/Ebl.inf

# Raw Files
FILE FREEFORM = A91D838E-A5FA-4138-825D-455E2303079E {
    SECTION UI = "BDS_Menu.cfg"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/BDS_Menu.cfg
}

FILE FREEFORM = A1E235DE-E825-4591-9623-C43175811826 {
    SECTION UI = "SecParti.cfg"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/SecParti.cfg
}

FILE FREEFORM = A91D838E-A5FA-4138-825D-455E23030794 {
    SECTION UI = "logo1.bmp"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/logo1.bmp
}

FILE FREEFORM = 03E9256F-E621-48D8-8576-7E3B4FCF2D41 {
    SECTION UI = "PanelSimConfig.csv"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/PanelSimConfig.csv
}

FILE FREEFORM = 21E9BDD9-6C3F-4F10-84A5-BBEC322741F1 {
    SECTION UI = "uefipil.cfg"
    SECTION RAW = $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/RawFiles/uefipil.cfg
}

###### FV2 - Console and User Interface ######
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SimpleTextInOutSerialDxe/SimpleTextInOutSerial.inf
INF MdeModulePkg/Universal/PrintDxe/PrintDxe.inf
INF MdeModulePkg/Universal/Console/ConPlatformDxe/ConPlatformDxe.inf
INF MdeModulePkg/Universal/Console/ConSplitterDxe/ConSplitterDxe.inf
INF MdeModulePkg/Universal/Console/GraphicsConsoleDxe/GraphicsConsoleDxe.inf

# Display
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/DisplayDxe/DisplayDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/FeatureEnablerDxe/FeatureEnablerDxe.inf

# I/O
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/SPIDxe/SPIDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/HSUartDxe/HSUartDxe.inf

# Power
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PmicDxe/PmicDxeLa.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PmicGlinkDxe/PmicGlinkDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/ChargerExDxe/ChargerExDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/QcomChargerDxe/QcomChargerDxeLA.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbPwrCtrlDxe/UsbPwrCtrlDxe.inf

# Sensors
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/TsensDxe/TsensDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/DDRInfoDxe/DDRInfoDxe.inf

# USB
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbfnDwc3Dxe/UsbfnDwc3Dxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/XhciPciEmulationDxe/XhciPciEmulationDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/XhciDxe/XhciDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbBusDxe/UsbBusDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbKbDxe/UsbKbDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbMassStorageDxe/UsbMassStorageDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbMsdDxe/UsbMsdDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbDeviceDxe/UsbDeviceDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbConfigDxe/UsbConfigDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UsbInitDxe/UsbInitDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/UCDxe/UCDxe.inf

# PIL
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PILDxe/PILDxe.inf
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/PILProxyDxe/PILProxyDxe.inf

# Utilities
INF $(PACKAGE_NAME)/Device/$(TARGET_DEVICE)/Binaries/QcomPkg/Drivers/FvUtilsDxe/FvUtilsEnhancedDxe.inf
