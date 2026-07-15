-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "number_of_approved_strata_lots"
FROM "sg-data-d-b0505f2a0218d38fdeaa6217753a0b68"
