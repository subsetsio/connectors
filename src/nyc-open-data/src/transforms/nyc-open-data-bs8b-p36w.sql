-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "job_number",
    "job_type",
    "c_o_issue_date",
    "bin_number",
    "borough",
    "number",
    "street",
    "block",
    "lot",
    "postcode",
    "pr_dwelling_unit",
    "ex_dwelling_unit",
    "application_status_raw",
    "filing_status_raw",
    "item_number",
    "issue_type",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-bs8b-p36w"
