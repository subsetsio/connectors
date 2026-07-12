-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This multiple-onset country-year file allows repeated country-years for simultaneous onsets; filter or group by conflict fields before aggregating.
SELECT
    "abc",
    "name",
    "year",
    "gwno_a",
    "newconf",
    "onset1",
    "onset2",
    "onset3",
    "onset5",
    "onset10",
    "onset20",
    "conflict_ids",
    "year_prev"
FROM "ucdp-onset-intrastate-country-multiple"
