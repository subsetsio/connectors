-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars_Ratio" AS milliondollars_ratio,
    "FinalDemand_Domesticexports_MillionDollars" AS finaldemand_domesticexports_milliondollars,
    "FinalDemand_Importrequirementsforexports_MillionDollars" AS finaldemand_importrequirementsforexports_milliondollars,
    "FinalDemand_Netforeignexchangeearnings_MillionDollars" AS finaldemand_netforeignexchangeearnings_milliondollars,
    "FinalDemand_Netforeignexchangeearningsasaproportionofdomesticex" AS finaldemand_netforeignexchangeearningsasaproportionofdomesticex
FROM "sg-data-d-8c0d9185b0480b41e69fdd2970e55f51"
