-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "type_of_international_protection",
    "type_of_proceedings",
    "indicator",
    "value"
FROM "statistics-estonia-lr16.px"
