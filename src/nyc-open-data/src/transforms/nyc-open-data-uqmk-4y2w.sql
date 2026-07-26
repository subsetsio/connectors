-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "survey",
    "prevalence",
    "_year" AS year,
    "smoked_at_least_once_past_30_days",
    "ever_had_a_drink_of_alcohol",
    "physically_active_at_least_60_minutes_per_day"
FROM "nyc-open-data-uqmk-4y2w"
