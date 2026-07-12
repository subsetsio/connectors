-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "place_of_residence",
    "sex",
    "place_of_birth",
    "age_group",
    "value"
FROM "statistics-estonia-rl0508.px"
