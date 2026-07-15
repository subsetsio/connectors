-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "no_of_active_claimants"
FROM "sg-data-d-ac37f9e1e46841a52f7c5324602d8bbd"
