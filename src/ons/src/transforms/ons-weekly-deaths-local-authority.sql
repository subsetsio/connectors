-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "administrative_geography",
    "geography",
    "week_number",
    "week",
    "cause_of_death",
    "causeofdeath",
    "place_of_death",
    "placeofdeath",
    "registration_or_occurrence",
    "registrationoroccurrence"
FROM "ons-weekly-deaths-local-authority"
