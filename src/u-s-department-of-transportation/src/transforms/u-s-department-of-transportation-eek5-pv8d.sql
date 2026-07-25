-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "state_name",
    "county_name",
    "city_name",
    "state_code",
    "state_fipcode",
    "county_code",
    "county_fipcode",
    "city_code",
    "city_fipcode"
FROM "u-s-department-of-transportation-eek5-pv8d"
