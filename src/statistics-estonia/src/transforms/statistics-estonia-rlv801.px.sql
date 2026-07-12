-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_and_tenure_status_of_dwelling",
    CAST("year" AS BIGINT) AS year,
    "sex",
    "ethnic_nationality",
    "age_group",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv801.px"
