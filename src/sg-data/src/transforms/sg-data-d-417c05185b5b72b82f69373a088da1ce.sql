-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nomination_day",
    "polling_day"
FROM "sg-data-d-417c05185b5b72b82f69373a088da1ce"
