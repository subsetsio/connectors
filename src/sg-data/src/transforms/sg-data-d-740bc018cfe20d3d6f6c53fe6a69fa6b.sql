-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "hdb_resident_population"
FROM "sg-data-d-740bc018cfe20d3d6f6c53fe6a69fa6b"
