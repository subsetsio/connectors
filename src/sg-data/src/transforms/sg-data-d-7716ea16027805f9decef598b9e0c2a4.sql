-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "scholarship_award",
    "description",
    "reference"
FROM "sg-data-d-7716ea16027805f9decef598b9e0c2a4"
