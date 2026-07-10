-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "State" AS state,
    "State Abbreviation" AS state_abbreviation,
    CAST("Median Number" AS DOUBLE) AS median_number,
    CAST("Lower Bound" AS DOUBLE) AS lower_bound,
    CAST("Upper Bound" AS DOUBLE) AS upper_bound,
    "Outcome" AS outcome,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Rolling 4-Week Mean" AS DOUBLE) AS rolling_4_week_mean,
    CAST("Rolling 4-Week Lower" AS DOUBLE) AS rolling_4_week_lower,
    CAST("Rolling 4-Week Upper" AS DOUBLE) AS rolling_4_week_upper,
    strptime("AnalysisDate", '%Y-%m-%d')::DATE AS analysisdate
FROM "cdc-v2g4-wqg2"
