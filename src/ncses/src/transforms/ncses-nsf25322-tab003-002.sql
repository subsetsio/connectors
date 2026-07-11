-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sector and occupation" AS sector_and_occupation,
    "Total" AS total,
    "Job satisfaction - Very satisfied" AS job_satisfaction_very_satisfied,
    "Job satisfaction - Somewhat satisfied" AS job_satisfaction_somewhat_satisfied,
    "Job satisfaction - Somewhat dissatisfied" AS job_satisfaction_somewhat_dissatisfied,
    "Job satisfaction - Very dissatisfied" AS job_satisfaction_very_dissatisfied
FROM "ncses-nsf25322-tab003-002"
