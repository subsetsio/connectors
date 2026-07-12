-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ability_to_speak_a_dialect",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "age_group",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv445.px"
