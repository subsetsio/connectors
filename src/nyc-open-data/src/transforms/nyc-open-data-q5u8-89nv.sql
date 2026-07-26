-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "license_status",
    "business_name",
    "dbatrade_name",
    "business_unique_id",
    "darp_enrollment_status",
    "rotow_enrollment_status",
    "building_number",
    "street",
    "unit_type",
    "unit",
    "city",
    "state",
    "zip_code",
    "borough",
    "community_board",
    "council_district",
    "police_precinct",
    "bin",
    "bbl",
    "nta",
    "census_block_2010",
    "census_tract_2010",
    "latitude",
    "longitude",
    "x_coordinate",
    "y_coordinate"
FROM "nyc-open-data-q5u8-89nv"
