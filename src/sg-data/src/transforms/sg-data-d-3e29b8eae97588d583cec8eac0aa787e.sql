-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "region",
    "cor",
    "age_group",
    "arv_count"
FROM "sg-data-d-3e29b8eae97588d583cec8eac0aa787e"
