-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type",
    "number_of_enforcement"
FROM "sg-data-d-6bba2359d86f90dbf5ba4d7bb55eb0c7"
