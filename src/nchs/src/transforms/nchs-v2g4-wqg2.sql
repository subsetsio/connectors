-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "state",
    "state_abbreviation",
    "median_number",
    "lower_bound",
    "upper_bound",
    "outcome",
    "mmwr_year",
    "mmwr_week",
    "rolling_4_week_mean",
    "rolling_4_week_lower",
    "rolling_4_week_upper",
    "analysisdate"
FROM "nchs-v2g4-wqg2"
