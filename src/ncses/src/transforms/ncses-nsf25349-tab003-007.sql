-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field and demographic characteristic" AS field_and_demographic_characteristic,
    "Age at doctorate median years" AS age_at_doctorate_median_years,
    "Doctorate recipients number" AS doctorate_recipients_number,
    "25 and under %" AS "25_and_under",
    "26–30 %" AS "26_30",
    "31–35 %" AS "31_35",
    "36–40 %" AS "36_40",
    "41–45 %" AS "41_45",
    "Over 45 %" AS over_45
FROM "ncses-nsf25349-tab003-007"
