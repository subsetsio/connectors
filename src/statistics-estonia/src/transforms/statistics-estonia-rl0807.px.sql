-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "indicator",
    "place_of_residence",
    "sex",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0807.px"
