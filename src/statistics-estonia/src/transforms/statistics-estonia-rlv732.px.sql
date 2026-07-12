-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "size_of_family",
    CAST("year" AS BIGINT) AS year,
    "type_of_family",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv732.px"
