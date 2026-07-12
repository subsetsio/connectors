-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "agricultural_product",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "value"
FROM "statistics-estonia-pm1901.px"
