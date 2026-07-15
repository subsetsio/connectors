-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "highest_qualification",
    "labour_force"
FROM "sg-data-d-cdb0d9a947bd381c7a767ed2fce1f99f"
