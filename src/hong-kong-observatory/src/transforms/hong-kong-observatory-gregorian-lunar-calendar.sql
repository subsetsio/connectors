-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The served Gregorian year window is rolling, so this reference table covers the calendar window currently exposed by the upstream API.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "lunar_year",
    "lunar_date"
FROM "hong-kong-observatory-gregorian-lunar-calendar"
