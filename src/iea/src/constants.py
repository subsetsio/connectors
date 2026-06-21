"""Dataset-id selections for the iea connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "BiofuelConsBySector", "Biotrans", "CO2ByGDP", "CO2ByGDPPPP", "CO2BySector",
    "CO2BySource", "CO2EleBySource", "CO2Industry", "CO2Intensity",
    "CO2IntensityPower", "CO2PerCap", "CO2Road", "CoalConsBySector",
    "CoalConsByType", "CoalImportsExports", "CoalProdByType", "CommPubBySource",
    "CrudeImportsExports", "DomesticProduction", "EEIManufacturing",
    "EEIPassengerTransport", "EEIREsidential", "EEIServices",
    "ETISharesInPowerGen", "ElecConsBySector", "ElecConsPerCapita",
    "ElecGenByFuel", "ElecGenByFuelLC", "ElecImportsExports", "ElecIndex",
    "FECI", "GasPrice", "HeatGenByFuel", "HydroGen", "IndustryBySource",
    "ManufacturingConsBySubsector", "NatGasCons", "NatGasConsBySector",
    "NatGasImportsExports", "NatGasProd", "NetImports", "NuclearGen",
    "NuclearHeat", "OilProd", "OilProductsCons", "OilProductsConsBySector",
    "PrimaryOilImportsExports", "RenewGenBySource", "ResidentialBySource",
    "ResidentialConsByEndUse", "SDG71", "SDG72", "SDG72modern", "SDG73",
    "SDG94", "SecondaryOilImportsExports", "ServicesConsByEndUse", "SolarGen",
    "TESbyGDP", "TESbyGDPPPP", "TESbyPop", "TESbySource", "TFCShareBySector",
    "TFCbySector", "TFCbySource", "TotCO2", "TotElecCons", "TransportBySource",
    "TransportConsBySubsector", "WasteGenBySource", "WasteHeatBySource",
    "WindGen", "emissionsDrivers",
]
