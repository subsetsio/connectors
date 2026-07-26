-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hh_id",
    "weight",
    "cms_zone",
    "survey_mode",
    "vehicle_num",
    "vehicle_id",
    "_year" AS year,
    "home_park",
    "home_park_amount_day",
    "home_park_amount_month",
    "home_park_amount_week",
    "home_park_amount_year"
FROM "nyc-open-data-jxs5-ygaz"
