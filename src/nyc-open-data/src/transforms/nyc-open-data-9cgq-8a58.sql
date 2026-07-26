-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year_of_submission_of_eer_to_dob",
    "facility_name",
    "address",
    "city",
    "zip_code",
    "agency",
    "bin",
    "bbl",
    "gross_square_footage",
    "bdbid",
    "unique_identifier",
    "measure",
    "measure_name",
    "measure_status",
    "measure_category",
    "estimated_installation_cost",
    "actual_cost_incurred_by_dcas11",
    "mtco2e_reduction",
    "reason_not_implemented",
    "simple_payback"
FROM "nyc-open-data-9cgq-8a58"
