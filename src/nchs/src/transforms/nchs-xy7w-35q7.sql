-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("analysisdate", '%m/%d/%Y')::DATE AS analysisdate,
    "hhs_region",
    "raceethnicity",
    "agegroup",
    "mmwryear",
    "mmwrweek",
    strptime("weekendingdate", '%m/%d/%Y')::DATE AS weekendingdate,
    "allcause",
    "covid_19_u071_multiple_cause_of_death",
    "covid_19_u071_underlying_cause_of_death",
    "flag_allcause",
    "flag_covidmcod",
    "flag_coviducod"
FROM "nchs-xy7w-35q7"
