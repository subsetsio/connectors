-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_ModeofTransport_CombinationsofRail_MRT_LRT_orPublicBus" AS total_modeoftransport_combinationsofrail_mrt_lrt_orpublicbus,
    "Total_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS total_modeoftransport_carortaxi_privatehirecaronly,
    "Total_ModeofTransport_OtherModes" AS total_modeoftransport_othermodes,
    "Total_ModeofTransport_NoTransportRequired" AS total_modeoftransport_notransportrequired,
    "CentralRegion_Total" AS centralregion_total,
    "CentralRegion_ModeofTransport_CombinationsofRail_MRT_LRT_orPubl" AS centralregion_modeoftransport_combinationsofrail_mrt_lrt_orpubl,
    "CentralRegion_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS centralregion_modeoftransport_carortaxi_privatehirecaronly,
    "CentralRegion_ModeofTransport_OtherModes" AS centralregion_modeoftransport_othermodes,
    "CentralRegion_ModeofTransport_NoTransportRequired" AS centralregion_modeoftransport_notransportrequired,
    "EastRegion_Total" AS eastregion_total,
    "EastRegion_ModeofTransport_CombinationsofRail_MRT_LRT_orPublicB" AS eastregion_modeoftransport_combinationsofrail_mrt_lrt_orpublicb,
    "EastRegion_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS eastregion_modeoftransport_carortaxi_privatehirecaronly,
    "EastRegion_ModeofTransport_OtherModes" AS eastregion_modeoftransport_othermodes,
    "EastRegion_ModeofTransport_NoTransportRequired" AS eastregion_modeoftransport_notransportrequired,
    "NorthRegion_Total" AS northregion_total,
    "NorthRegion_ModeofTransport_CombinationsofRail_MRT_LRT_orPublic" AS northregion_modeoftransport_combinationsofrail_mrt_lrt_orpublic,
    "NorthRegion_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS northregion_modeoftransport_carortaxi_privatehirecaronly,
    "NorthRegion_ModeofTransport_OtherModes" AS northregion_modeoftransport_othermodes,
    "NorthRegion_ModeofTransport_NoTransportRequired" AS northregion_modeoftransport_notransportrequired,
    "North_EastRegion_Total" AS north_eastregion_total,
    "North_EastRegion_ModeofTransport_CombinationsofRail_MRT_LRT_orP" AS north_eastregion_modeoftransport_combinationsofrail_mrt_lrt_orp,
    "North_EastRegion_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS north_eastregion_modeoftransport_carortaxi_privatehirecaronly,
    "North_EastRegion_ModeofTransport_OtherModes" AS north_eastregion_modeoftransport_othermodes,
    "North_EastRegion_ModeofTransport_NoTransportRequired" AS north_eastregion_modeoftransport_notransportrequired,
    "WestRegion_Total" AS westregion_total,
    "WestRegion_ModeofTransport_CombinationsofRail_MRT_LRT_orPublicB" AS westregion_modeoftransport_combinationsofrail_mrt_lrt_orpublicb,
    "WestRegion_ModeofTransport_CarorTaxi_PrivateHireCarOnly" AS westregion_modeoftransport_carortaxi_privatehirecaronly,
    "WestRegion_ModeofTransport_OtherModes" AS westregion_modeoftransport_othermodes,
    "WestRegion_ModeofTransport_NoTransportRequired" AS westregion_modeoftransport_notransportrequired
FROM "sg-data-d-5b38192e9c6f8d2c5f38c70939c76e71"
