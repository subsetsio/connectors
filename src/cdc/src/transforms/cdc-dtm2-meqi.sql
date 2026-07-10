-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    "Jurisdiction of Occurrence" AS jurisdiction_of_occurrence,
    "Urban-Rural Classification" AS urban_rural_classification,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "Time Period" AS time_period,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("Drug Overdose Deaths" AS BIGINT) AS drug_overdose_deaths
FROM "cdc-dtm2-meqi"
