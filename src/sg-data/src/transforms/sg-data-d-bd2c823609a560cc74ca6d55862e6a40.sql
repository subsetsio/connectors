-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars_Ratio" AS milliondollars_ratio,
    "NetForeignExchangeEarningsFromExports_Exports_MillionDollars" AS netforeignexchangeearningsfromexports_exports_milliondollars,
    "NetForeignExchangeEarningsFromExports_Importrequirementsforexpo" AS netforeignexchangeearningsfromexports_importrequirementsforexpo,
    "NetForeignExchangeEarningsFromExports_Netforeignexchangeearning" AS netforeignexchangeearningsfromexports_netforeignexchangeearning,
    "NetForeignExchangeEarningsFromExports_Netforeignexchangeearning_1" AS netforeignexchangeearningsfromexports_netforeignexchangeearning_1
FROM "sg-data-d-bd2c823609a560cc74ca6d55862e6a40"
