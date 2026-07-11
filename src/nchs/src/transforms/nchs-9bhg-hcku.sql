-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "group",
    "year",
    "month",
    "state",
    "sex",
    "age_group",
    "covid_19_deaths",
    "total_deaths",
    "pneumonia_deaths",
    "pneumonia_and_covid_19_deaths",
    "influenza_deaths",
    "pneumonia_influenza_or_covid_19_deaths",
    "footnote"
FROM "nchs-9bhg-hcku"
