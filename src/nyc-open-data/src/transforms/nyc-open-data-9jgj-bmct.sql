-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "complaint_number",
    "incident_address_street_number",
    "incident_address_street_name",
    "incident_address",
    "incident_address_zip",
    "incident_address_borough",
    "complaint_type_311",
    "descriptor_1_311",
    "complaint_status",
    "date_received",
    "deleted",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-9jgj-bmct"
