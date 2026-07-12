-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "family_nucleus_composition",
    "number_and_age_of_children",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl527.px"
