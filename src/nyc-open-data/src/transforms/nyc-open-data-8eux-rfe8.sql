-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "file_name",
    "input_1_buildingnumber",
    "service_type",
    "service_category",
    "input_1_facilityname",
    "input_1_address",
    "input_2__address" AS input_2_address,
    "building_number",
    "input_1_borough",
    "input_1_zipcode",
    "latitude2",
    "longitude2",
    "input_1_phone2",
    "column3",
    "input_1_additionalinfo2",
    "output_bbl",
    "output_bin",
    "output_city_council_district",
    "output_community_district",
    "output_nta_name",
    "_location" AS location
FROM "nyc-open-data-8eux-rfe8"
