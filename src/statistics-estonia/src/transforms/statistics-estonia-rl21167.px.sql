-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_of_place_of_work",
    "sex",
    "occupation",
    "place_of_residence",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl21167.px"
