-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "device_number",
    "device_type",
    "device_status",
    "status_date",
    "equipment_type",
    "periodic_report_year",
    "cat1_report_year",
    "cat1_latest_report_filed_date",
    "cat5_latest_report_filed_date",
    "periodic_latest_inspection_date",
    "bin",
    "borough",
    "house_number",
    "street_name",
    "block",
    "lot",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-e5aq-a4j2"
