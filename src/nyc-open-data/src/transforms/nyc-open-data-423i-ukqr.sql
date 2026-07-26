-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_year",
    "agency_name",
    "equal_employment_opportunity_eeo4_job_category",
    "pay_band",
    "lower_pay_band_bound",
    "upper_pay_band_bound",
    "employee_status",
    "race",
    "ethnicity",
    "gender",
    "number_of_employees"
FROM "nyc-open-data-423i-ukqr"
