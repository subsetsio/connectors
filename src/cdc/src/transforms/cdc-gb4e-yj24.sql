-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data as of" AS data_as_of,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "ST_ABBREV" AS st_abbrev,
    "STATE_NAME" AS state_name,
    "COUNTYNAME" AS countyname,
    CAST("FIPS" AS BIGINT) AS fips,
    "STATEFIPS" AS statefips,
    "COUNTYFIPS" AS countyfips,
    CAST("CODE2013" AS BIGINT) AS code2013,
    CAST("Provisional Drug Overdose Deaths" AS BIGINT) AS provisional_drug_overdose_deaths,
    "Footnote" AS footnote,
    CAST("Percentage Of Records Pending Investigation" AS DOUBLE) AS percentage_of_records_pending_investigation,
    "HistoricalDataCompletenessNote" AS historicaldatacompletenessnote,
    strptime("MonthEndingDate", '%m/%d/%Y')::DATE AS monthendingdate,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cdc-gb4e-yj24"
