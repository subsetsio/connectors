-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "number_of_flats_in_the_building",
    "location",
    "value"
FROM "statistics-estonia-rlv211.px"
