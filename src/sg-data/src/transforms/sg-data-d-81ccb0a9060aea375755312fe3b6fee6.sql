-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "labour_force_status",
    "labour_force_status_distribution"
FROM "sg-data-d-81ccb0a9060aea375755312fe3b6fee6"
