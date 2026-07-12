-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "duration_of_annual_stay_at_the_secondary_place_of_residence",
    "sex",
    "secondary_place_of_residence",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0327.px"
