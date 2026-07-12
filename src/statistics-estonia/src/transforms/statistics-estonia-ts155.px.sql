-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "nationality_of_vessel",
    "type_of_vessel",
    "direction",
    "indicator",
    "value"
FROM "statistics-estonia-ts155.px"
