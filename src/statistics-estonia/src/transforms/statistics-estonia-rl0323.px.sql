-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "sex",
    "secondary_place_of_residence",
    "ethnic_nationality",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0323.px"
