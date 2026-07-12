-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "household_size",
    "sex",
    "age",
    "importance_of_source_of_subsistence",
    "source_of_subsistence",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl506.px"
