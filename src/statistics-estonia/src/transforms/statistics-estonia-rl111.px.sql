-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "place_of_residence_1989",
    "place_of_residence_estonia_2000",
    "sex",
    "value"
FROM "statistics-estonia-rl111.px"
