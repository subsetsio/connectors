-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citizenship",
    "household_structure",
    "place_of_residence",
    "indicator",
    "value"
FROM "statistics-estonia-rl0717.px"
