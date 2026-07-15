-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "qtr",
    "no_of_active_mbrs"
FROM "sg-data-d-89dd4e5486fe3bb3b0c620cc6f787cdc"
