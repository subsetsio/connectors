-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "aim_of_library_visit",
    CAST("year" AS BIGINT) AS year,
    "place_of_residence_group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-kut025.px"
