-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ethnic_group",
    "single_parent_births",
    "teenage_births"
FROM "sg-data-d-9df8d9f4545fa651b4be4614b4762f4c"
