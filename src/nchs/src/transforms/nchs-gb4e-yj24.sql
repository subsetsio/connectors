-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "year",
    "month",
    "st_abbrev",
    "state_name",
    "countyname",
    "fips",
    "statefips",
    "countyfips",
    "code2013",
    "provisional_drug_overdose_deaths",
    "footnote",
    "percentage_of_records_pending_investigation",
    "historicaldatacompletenessnote",
    strptime("monthendingdate", '%m/%d/%Y')::DATE AS monthendingdate,
    strptime("start_date", '%m/%d/%Y')::DATE AS start_date,
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date
FROM "nchs-gb4e-yj24"
