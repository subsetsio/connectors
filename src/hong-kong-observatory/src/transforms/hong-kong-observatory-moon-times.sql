-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows contain daily moonrise, moon transit, and moonset times for Hong Kong; some event fields may be blank when that event does not occur on the civil date.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "rise",
    "transit",
    "set"
FROM "hong-kong-observatory-moon-times"
