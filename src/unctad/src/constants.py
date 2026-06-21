"""Dataset-id selections for the unctad connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "US.BioTradeMerchGDPShare", "US.BiotradeMerchRCA",
    "US.BiotradeMerchShare", "US.ConcentDiversIndices", "US.ConcentStructIndices",
    "US.ContPortThroughput", "US.Cpi_A", "US.CreativeGoodsGR", "US.CreativeGoodsValue",
    "US.CreativeServ_Group_E", "US.CreativeServ_Indiv_Tot", "US.CurrAccBalance",
    "US.DigitallyDeliverableServices", "US.ECommerceInternational", "US.ECommerceTotal",
    "US.EnvironmentalGoodsRCA", "US.EnvironmentalGoodsTrade", "US.ExchangeRateCrosstab",
    "US.FTRI", "US.FdiFlowsStock", "US.FleetBeneficialOwners", "US.GDPComponent",
    "US.GDPGR", "US.GDPTotal", "US.GNI", "US.Gender_DomesticValueAdded",
    "US.Gender_TradableIndustries", "US.GoodsAndServBalanceBpm6",
    "US.GoodsAndServTradeOpennessBpm6", "US.GoodsAndServicesBpm6",
    "US.IFF_CrimesRelated_In", "US.IFF_CrimesRelated_Out", "US.IFF_TradeMisinvoicing_In",
    "US.IFF_TradeMisinvoicing_Out", "US.IctGoodsShare", "US.IctGoodsValue",
    "US.IctProductionSector", "US.IctUseEconActivity", "US.IctUseEconActivity_Isic4",
    "US.IctUseEnterprSize", "US.IctUseLocation", "US.IntraTrade", "US.LSBCI",
    "US.LSCI", "US.LSCI_M", "US.MerchTheilIndices", "US.MerchVolumeQuarterly",
    "US.MerchantFleet", "US.OceanServices", "US.OceanTrade", "US.PCI", "US.PLSCI",
    "US.PlasticsTradebyPartner", "US.PopAgeStruct", "US.PopDependency", "US.PopTotal",
    "US.PortCalls", "US.PortCallsArrivals", "US.PortCallsArrivals_S", "US.PortCalls_S",
    "US.RCA", "US.Remittances", "US.SDG_LULFRG", "US.SDG_PORFVOL", "US.SeaborneTrade",
    "US.ShipBuilding", "US.ShipScrapping", "US.Tariff", "US.TermsOfTrade",
    "US.TotAndComServicesQuarterly", "US.TradeServCatByPartner",
    "US.TradeServCatQuarterlyAnnualized", "US.TradeServCatTotal", "US.TradeServICT",
    "US.TradeMerchBalance", "US.TradeMerchGR", "US.TradeMerchTotal", "US.UCPI_A",
    "US.UCPI_M", "US.VesselValueByOwnership", "US.VesselValueByRegistration",
]
