-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an anonymized case line list for a concluded outbreak; dates describe case lifecycle and record entry events rather than a uniform observation period.
SELECT
    CAST("ID" AS BIGINT) AS id,
    "Pathogen" AS pathogen,
    "Country" AS country,
    "Country_ISO3" AS country_iso3,
    "Case_status" AS case_status,
    "Confirmation_method" AS confirmation_method,
    "Healthcare_worker" AS healthcare_worker,
    "Occupation" AS occupation,
    "Gender" AS gender,
    "Age" AS age,
    "Date_onset" AS date_onset,
    "Date_onset_estimated" AS date_onset_estimated,
    "Outcome" AS outcome,
    "Date_of_first_consult" AS date_of_first_consult,
    "Date_death" AS date_death,
    "Date_recovered" AS date_recovered,
    "Location_Province" AS location_province,
    "Location_District" AS location_district,
    "Contact_with_case" AS contact_with_case,
    "Source" AS source,
    "Date_entry" AS date_entry,
    "Data_up_to" AS data_up_to
FROM "global-health-marburg-equatorial-guinea-2023"
