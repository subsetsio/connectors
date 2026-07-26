-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tracking_number",
    "boiler_id",
    "report_type",
    "applicantfirst_name",
    "applicant_last_name",
    "applicant_license_type",
    "applicant_license_number",
    "owner_first_name",
    "owner_last_name",
    "boiler_make",
    "boiler_model",
    "pressure_type",
    "inspection_type",
    "inspection_date",
    "defects_exist",
    "lff_45_days",
    "lff_180_days",
    "filing_fee",
    "total_amount_paid",
    "report_status",
    "bin_number"
FROM "nyc-open-data-52dp-yji6"
