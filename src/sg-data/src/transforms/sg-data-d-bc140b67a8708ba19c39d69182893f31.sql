-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "carbon_intensity_of_electricity_generation"
FROM "sg-data-d-bc140b67a8708ba19c39d69182893f31"
