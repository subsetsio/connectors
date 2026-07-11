-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    "start_date",
    "end_date",
    "group",
    "year",
    "month",
    "mmwr_week",
    "weekending_date",
    "state",
    "demographic_type",
    "demographic_values",
    "pathogen",
    "deaths",
    "total_deaths",
    "percent_deaths",
    "provisional",
    "suppressed"
FROM "nchs-53g5-jf7x"
