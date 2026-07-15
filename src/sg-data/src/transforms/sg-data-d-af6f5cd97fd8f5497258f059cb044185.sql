-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "percentage_psle_science"
FROM "sg-data-d-af6f5cd97fd8f5497258f059cb044185"
