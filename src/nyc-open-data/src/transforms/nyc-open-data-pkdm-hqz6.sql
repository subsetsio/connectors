-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "job_filing_name",
    "job_type",
    "bin",
    "borough",
    "house_no",
    "street_name",
    "block",
    "lot",
    "zip_code",
    "submitted_date",
    "c_of_o_status",
    "c_of_o_sequence",
    "c_of_o_filing_type",
    "community_board",
    "c_of_o_issuance_date",
    "application_number",
    "number_of_dwelling_units",
    "c_of_o_number",
    "latitude",
    "longitude",
    "council_district",
    "bbl",
    "census_tract",
    "nta"
FROM "nyc-open-data-pkdm-hqz6"
