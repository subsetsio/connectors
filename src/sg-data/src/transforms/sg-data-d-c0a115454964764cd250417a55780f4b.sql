-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "region",
    "cor",
    "moa",
    "arv_count"
FROM "sg-data-d-c0a115454964764cd250417a55780f4b"
