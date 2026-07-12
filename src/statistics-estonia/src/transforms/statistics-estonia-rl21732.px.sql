-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "size_of_family",
    "type_of_family",
    "place_of_residence",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl21732.px"
