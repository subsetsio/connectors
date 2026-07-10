-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Major_code" AS major_code,
    "Major" AS major,
    "Major_category" AS major_category,
    "Grad_total" AS grad_total,
    "Grad_sample_size" AS grad_sample_size,
    "Grad_employed" AS grad_employed,
    "Grad_full_time_year_round" AS grad_full_time_year_round,
    "Grad_unemployed" AS grad_unemployed,
    "Grad_unemployment_rate" AS grad_unemployment_rate,
    "Grad_median" AS grad_median,
    "Grad_P25" AS grad_p25,
    "Grad_P75" AS grad_p75,
    "Nongrad_total" AS nongrad_total,
    "Nongrad_employed" AS nongrad_employed,
    "Nongrad_full_time_year_round" AS nongrad_full_time_year_round,
    "Nongrad_unemployed" AS nongrad_unemployed,
    "Nongrad_unemployment_rate" AS nongrad_unemployment_rate,
    "Nongrad_median" AS nongrad_median,
    "Nongrad_P25" AS nongrad_p25,
    "Nongrad_P75" AS nongrad_p75,
    "Grad_share" AS grad_share,
    "Grad_premium" AS grad_premium
FROM "fivethirtyeight-college-majors-grad-students"
