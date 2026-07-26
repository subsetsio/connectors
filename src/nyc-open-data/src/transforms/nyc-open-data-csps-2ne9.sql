-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "school_name",
    "school_type",
    "school_level",
    "regents_exam",
    "_year" AS year,
    "demographic_category",
    "demographic_variable",
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
FROM "nyc-open-data-csps-2ne9"
