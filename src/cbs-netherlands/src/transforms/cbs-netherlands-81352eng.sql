-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SIC2008" AS sic2008,
    "Periods" AS periods,
    "InvestmentsInTangibleFixedAssets_1" AS investmentsintangiblefixedassets_1,
    "Land_2" AS land_2,
    "CorporateBuildings_3" AS corporatebuildings_3,
    "NetworkInfrastructure_4" AS networkinfrastructure_4,
    "MeansOfTransport_5" AS meansoftransport_5,
    "ComputerHardwarePeripheralEquipment_6" AS computerhardwareperipheralequipment_6,
    "MachineryAndInstallations_7" AS machineryandinstallations_7,
    "OtherTangibleFixedAssets_8" AS othertangiblefixedassets_8,
    "NewTangibleFixedAssets_9" AS newtangiblefixedassets_9,
    "SecondHandTangibleFixedAssets_10" AS secondhandtangiblefixedassets_10,
    "DisposalOfTangibleFixedAssets_11" AS disposaloftangiblefixedassets_11,
    "SIC2008_label" AS sic2008_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81352eng"
