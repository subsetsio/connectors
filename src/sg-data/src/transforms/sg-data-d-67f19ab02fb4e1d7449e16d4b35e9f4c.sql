-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "region",
    "cor",
    "first",
    "repeat",
    "not_stated"
FROM "sg-data-d-67f19ab02fb4e1d7449e16d4b35e9f4c"
