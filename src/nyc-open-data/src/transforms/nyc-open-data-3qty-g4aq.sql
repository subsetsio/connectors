-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "survey",
    "prevalence",
    "_year" AS year,
    "smoked_at_least_once_past_30_days",
    "binge_drinking_in_past_30_days",
    "drank_five_or_more_alcoholic_drinks_in_a_row_in_past_30_days",
    "got_help_from_a_counselor_in_past_12_months",
    "drinks_1_or_more_sodas_per_day_in_past_7_days",
    "adolescent_obesity",
    "physically_active_60_minutes_per_day"
FROM "nyc-open-data-3qty-g4aq"
