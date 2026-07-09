-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "cv",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "travel_to_work_area",
    "geography",
    "averages_and_percentiles",
    "averagesandpercentiles",
    "sex",
    "sex_1",
    "working_pattern",
    "workingpattern",
    "hours_and_earnings",
    "hoursandearnings",
    "workplace_or_residence",
    "workplaceorresidence"
FROM "ons-ashe-tables-11-and-12"
