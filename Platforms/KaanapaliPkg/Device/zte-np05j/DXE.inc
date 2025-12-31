# DXE - Driver Execution Environment

# DXE Core
FILE DXE_CORE = 5AE3F37E-4EAE-41AE-8240-35465B5E81EB {
    SECTION PE32 = MdeModulePkg/Core/Dxe/DxeMain/DEBUG/DxeCore.efi
}

# TODO: Add device-specific DXE drivers from Binaries/ directory
# This will be populated after successful binary extraction
# For now, relying on DSC build to compile drivers from source
