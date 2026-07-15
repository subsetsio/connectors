-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pharmacy_name",
    "pharmacist_in_charge",
    "pharmacy_address"
FROM "sg-data-d-bc50d72a9d61457964c6ea8d8ba7dce2"
