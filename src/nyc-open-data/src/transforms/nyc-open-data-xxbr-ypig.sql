-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "job_number",
    "filing_type_name",
    "filing_number",
    "filing_status_name",
    "permit_number",
    "filing_date",
    "permit_issued_date",
    "permit_expiration_date",
    "laasign_off_date",
    "work_type_name",
    "location_bin",
    "location_house_no",
    "location_street_name",
    "location_borough_name",
    "proposed_work_summary",
    "building_type_name",
    "inspection_type_name",
    "inspection_date",
    "latitude",
    "longitude",
    "zip_code",
    "community_board",
    "council_district",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-xxbr-ypig"
