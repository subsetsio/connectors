-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    "Jurisdiction" AS jurisdiction,
    "Group" AS group,
    "Subgroup" AS subgroup,
    CAST("Year of Death" AS BIGINT) AS year_of_death,
    CAST("Month of Death" AS BIGINT) AS month_of_death,
    "Time Period" AS time_period,
    strptime("Month Ending Date", '%m/%d/%Y')::DATE AS month_ending_date,
    CAST("Maternal Deaths" AS BIGINT) AS maternal_deaths,
    CAST("Live Births" AS BIGINT) AS live_births,
    CAST("Maternal Mortality Rate" AS DOUBLE) AS maternal_mortality_rate,
    "Footnote" AS footnote
FROM "cdc-e2d5-ggg7"
