-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "bunker_type",
    "bunker_sales"
FROM "sg-data-d-4f5abbf4486bf8e52bbed3be56dde562"
