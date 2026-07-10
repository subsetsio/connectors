-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geom_id",
    "cartodb_id",
    "geom_webmercator_id",
    "municipality_id",
    "state",
    "cnpj_cpf",
    "company",
    "capacity",
    "point",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "subclass",
    "dt"
FROM "base-dos-dados-br-trase-supply-chain--soy-beans-storage-facilities"
