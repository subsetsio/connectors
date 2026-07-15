-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "contributiontype",
    "amount"
FROM "sg-data-d-50c329c8a3d698b1b5607896163fa38f"
