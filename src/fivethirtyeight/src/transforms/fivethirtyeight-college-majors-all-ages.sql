-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Major_code" AS major_code,
    "Major" AS major,
    "Major_category" AS major_category,
    "Total" AS total,
    "Employed" AS employed,
    "Employed_full_time_year_round" AS employed_full_time_year_round,
    "Unemployed" AS unemployed,
    "Unemployment_rate" AS unemployment_rate,
    "Median" AS median,
    "P25th" AS p25th,
    "P75th" AS p75th
FROM "fivethirtyeight-college-majors-all-ages"
