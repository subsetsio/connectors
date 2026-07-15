-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ind1",
    "ind2",
    "twc"
FROM "sg-data-d-e5848828d6a14d35a8b7eea7e15a149e"
