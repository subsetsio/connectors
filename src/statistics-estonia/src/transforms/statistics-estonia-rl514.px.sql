-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_economically_active_members",
    "household_composition",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl514.px"
