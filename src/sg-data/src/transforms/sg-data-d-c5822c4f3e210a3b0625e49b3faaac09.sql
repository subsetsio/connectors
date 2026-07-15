-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "company_licensee_name",
    "valid_period",
    "retail_outlet_address"
FROM "sg-data-d-c5822c4f3e210a3b0625e49b3faaac09"
