-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide employment table; columns encode income groups, industry slices, and weighting variants, so compare like-named measures rather than summing across all emp_* columns.
SELECT
    "year",
    "month",
    "day_endofweek",
    "emp",
    "emp_incq1",
    "emp_incq2",
    "emp_incq3",
    "emp_incq4",
    "emp_incmiddle",
    "emp_incbelowmed",
    "emp_incabovemed",
    "emp_subset_unweighted_q1",
    "emp_subset_unweighted_q2",
    "emp_subset_unweighted_q3",
    "emp_subset_unweighted_q4",
    "emp_subset_reweighted_q1",
    "emp_subset_reweighted_q2",
    "emp_subset_reweighted_q3",
    "emp_retail",
    "emp_s72",
    "emp_retail_inclow",
    "emp_retail_incmiddle",
    "emp_retail_inchigh",
    "emp_ss40",
    "emp_ss60",
    "emp_ss65",
    "emp_ss70"
FROM "opportunity-insights-tracker-employment-national-weekly"
