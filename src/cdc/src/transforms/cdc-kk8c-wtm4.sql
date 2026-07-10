-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Figure" AS BIGINT) AS figure,
    "Interview Period" AS interview_period,
    "Interview Dates" AS interview_dates,
    "Measure" AS measure,
    "Group" AS group,
    "Subgroup" AS subgroup,
    CAST("Percent" AS DOUBLE) AS percent,
    CAST("Lower 95% CI" AS DOUBLE) AS lower_95_ci,
    CAST("Upper 95% CI" AS DOUBLE) AS upper_95_ci,
    "Estimate Reliable?" AS estimate_reliable,
    "Estimate's Complement Reliable?" AS estimate_s_complement_reliable
FROM "cdc-kk8c-wtm4"
