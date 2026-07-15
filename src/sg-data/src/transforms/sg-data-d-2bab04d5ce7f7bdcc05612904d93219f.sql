-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "patient_type",
    "asir",
    "aspr"
FROM "sg-data-d-2bab04d5ce7f7bdcc05612904d93219f"
