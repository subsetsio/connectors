-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "country_code",
    "commodity",
    "commodity_code",
    "indicator",
    CAST("indicator_code" AS BIGINT) AS indicator_code,
    "unit",
    "frequency",
    "date",
    "value"
FROM "afdb-onszrad"
