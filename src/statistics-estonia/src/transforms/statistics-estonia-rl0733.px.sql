-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_and_number_of_children",
    "type_of_family",
    "household_structure",
    "county",
    "indicator",
    "value"
FROM "statistics-estonia-rl0733.px"
