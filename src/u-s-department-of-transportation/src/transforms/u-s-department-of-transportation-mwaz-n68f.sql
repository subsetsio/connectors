-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    "statistic",
    CAST("year" AS BIGINT) AS year,
    "value",
    "units"
FROM "u-s-department-of-transportation-mwaz-n68f"
