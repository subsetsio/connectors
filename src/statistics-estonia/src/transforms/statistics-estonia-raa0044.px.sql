-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "component",
    "indicator",
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "institutional_sector",
    "value"
FROM "statistics-estonia-raa0044.px"
