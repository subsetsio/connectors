-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "figure",
    "interview_period",
    "interview_dates",
    "measure",
    "group",
    "subgroup",
    "percent",
    "lower_95_ci",
    "upper_95_ci",
    "estimate_reliable",
    "estimate_s_complement_reliable"
FROM "nchs-kk8c-wtm4"
