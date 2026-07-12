-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "command_of_foreign_languages",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "ethnic_nationality",
    "age_group",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv444.px"
