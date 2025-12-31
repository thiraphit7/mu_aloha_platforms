# DXE - Driver Execution Environment
# Minimal configuration using only AndromedaPkg drivers

INF AndromedaPkg/Driver/RamPartitionDxe/RamPartitionDxe.inf
INF AndromedaPkg/Driver/SimpleFbDxe/SimpleFbDxe.inf

# TODO: Add device-specific DXE drivers from Binaries/ directory when available
# The DXE core and standard drivers are automatically included from APRIORI.inc and DXE.dsc.inc
