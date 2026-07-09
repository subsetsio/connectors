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
    "administrative_geography",
    "geography",
    "averages_and_percentiles",
    "averagesandpercentiles",
    "sic_unofficial",
    "unofficialstandardindustrialclassification",
    "hours_and_earnings",
    "hoursandearnings",
    "sex",
    "sex_1",
    "working_pattern",
    "workingpattern"
FROM "ons-ashe-table-5"
