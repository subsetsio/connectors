-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Rank" AS rank,
    "Major_code" AS major_code,
    "Major" AS major,
    "Total" AS total,
    "Men" AS men,
    "Women" AS women,
    "Major_category" AS major_category,
    "ShareWomen" AS sharewomen,
    "Sample_size" AS sample_size,
    "Employed" AS employed,
    "Full_time" AS full_time,
    "Part_time" AS part_time,
    "Full_time_year_round" AS full_time_year_round,
    "Unemployed" AS unemployed,
    "Unemployment_rate" AS unemployment_rate,
    "Median" AS median,
    "P25th" AS p25th,
    "P75th" AS p75th,
    "College_jobs" AS college_jobs,
    "Non_college_jobs" AS non_college_jobs,
    "Low_wage_jobs" AS low_wage_jobs
FROM "fivethirtyeight-college-majors-recent-grads"
