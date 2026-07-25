-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("number" AS BIGINT) AS number,
    CAST("year" AS BIGINT) AS year,
    "kode",
    "region",
    "municipalities",
    "total",
    "urban",
    "rural"
FROM "rosstat-7708234640-population"
