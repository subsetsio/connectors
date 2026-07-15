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
FROM "sg-data-d-b666f7cce17aa60b20f268dc27dfb742"
