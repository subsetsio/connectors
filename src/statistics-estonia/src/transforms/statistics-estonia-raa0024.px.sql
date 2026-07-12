-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "component",
    "value"
FROM "statistics-estonia-raa0024.px"
