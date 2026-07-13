-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    CAST("year" AS BIGINT) AS year,
    "indicator",
    "sector",
    CAST("value" AS BIGINT) AS value,
    "normalization",
    "source_resource"
FROM "idb-priorities-for-productivity-and-income-ppis-database"
