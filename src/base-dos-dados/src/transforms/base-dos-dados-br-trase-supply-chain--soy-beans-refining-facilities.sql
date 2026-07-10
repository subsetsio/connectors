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
    "company",
    "capacity",
    "point"
FROM "base-dos-dados-br-trase-supply-chain--soy-beans-refining-facilities"
