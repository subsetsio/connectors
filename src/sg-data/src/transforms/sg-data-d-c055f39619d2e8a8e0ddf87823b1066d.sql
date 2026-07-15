-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "mthly_payout_amt"
FROM "sg-data-d-c055f39619d2e8a8e0ddf87823b1066d"
