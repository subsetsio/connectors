-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    "year",
    "start_week",
    "end_week",
    "jurisdiction_of_residence",
    "age_group",
    "covid_19_deaths",
    "total_deaths"
FROM "nchs-mawz-airi"
