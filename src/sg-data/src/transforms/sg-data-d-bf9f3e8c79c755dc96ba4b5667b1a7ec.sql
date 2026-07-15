-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars_Ratio" AS milliondollars_ratio,
    "NetForeignExchangeEarningsFromExports_Domesticexports_MillionDo" AS netforeignexchangeearningsfromexports_domesticexports_milliondo,
    "NetForeignExchangeEarningsFromExports_Importrequirementsforexpo" AS netforeignexchangeearningsfromexports_importrequirementsforexpo,
    "NetForeignExchangeEarningsFromExports_Netforeignexchangeearning" AS netforeignexchangeearningsfromexports_netforeignexchangeearning,
    "NetForeignExchangeEarningsFromExports_Netforeignexchangeearning_1" AS netforeignexchangeearningsfromexports_netforeignexchangeearning_1
FROM "sg-data-d-bf9f3e8c79c755dc96ba4b5667b1a7ec"
