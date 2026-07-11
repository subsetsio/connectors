-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "state",
    "mmwr_week",
    strptime("end_week", '%m/%d/%Y')::DATE AS end_week,
    "sex",
    "age_group",
    "total_deaths",
    "covid_19_deaths"
FROM "nchs-vsak-wrfu"
