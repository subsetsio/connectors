-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "current_activity_status",
    CAST("year" AS BIGINT) AS year,
    "sex",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv132.px"
