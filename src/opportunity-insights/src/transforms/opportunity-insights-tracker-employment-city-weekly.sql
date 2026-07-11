-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day_endofweek",
    "cityid",
    "emp",
    "emp_incq1",
    "emp_incq2",
    "emp_incq3",
    "emp_incq4",
    "emp_incmiddle",
    "emp_incbelowmed",
    "emp_incabovemed"
FROM "opportunity-insights-tracker-employment-city-weekly"
