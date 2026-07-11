-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows contain daily sunrise, sun transit, and sunset times for Hong Kong.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "rise",
    "transit",
    "set"
FROM "hong-kong-observatory-sun-times"
