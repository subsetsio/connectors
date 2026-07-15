-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "no_of_active_claimants"
FROM "sg-data-d-2d354cff56f6a04bb55490fc92fa771e"
