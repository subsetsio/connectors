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
    "address",
    "slaugtherhouse_id",
    "company",
    "other_company_names",
    "multifunctions",
    "resolution_id",
    "subclass",
    "inspection_level",
    "inspection_number",
    "tac",
    "status",
    strptime("date_sif_registered", '%Y-%m-%d')::DATE AS date_sif_registered,
    "sif_category",
    "point"
FROM "base-dos-dados-br-trase-supply-chain--beef-slaughterhouses"
