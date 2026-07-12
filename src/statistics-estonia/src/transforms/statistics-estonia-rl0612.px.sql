-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ethnic_nationality",
    "extent_of_limitation",
    "place_of_residence",
    "age_group",
    "sex",
    "value"
FROM "statistics-estonia-rl0612.px"
