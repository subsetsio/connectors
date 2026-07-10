-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "name",
    "total",
    "male_share",
    "female_share",
    "gap"
FROM "fivethirtyeight-unisex-names-unisex-names-table"
