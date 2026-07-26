-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lookup",
    "school_dbn",
    "schoolname",
    "schooltype",
    "schoollevel",
    "regents_exam",
    "_year" AS year,
    "total_tested",
    "mean_score",
    "number_scoring_below_65",
    "percent_scoring_below_65",
    "number_scoring_65_or_above",
    "percent_scoring_65_or_above",
    "number_scoring_80_or_above",
    "percent_scoring_80_or_above",
    "number_scoring_cr",
    "percent_scoring_cr"
FROM "nyc-open-data-cbrh-qrk4"
