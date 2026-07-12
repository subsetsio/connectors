-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "quarter",
    "type_of_transport",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-ts101.px"
