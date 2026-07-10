-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "geom_id",
    "cartodb_id",
    "geom_webmercator_id",
    "municipality_id",
    "state",
    "crushing_facility_Id" AS crushing_facility_id,
    "cnpj",
    "company",
    "capacity",
    "capacity_source",
    "status",
    "point"
FROM "base-dos-dados-br-trase-supply-chain--soy-beans-crushing-facilities"
