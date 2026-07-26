-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_of_inspection",
    "inspection_number",
    "date_of_occurrence",
    "business_unique_id",
    "business_name",
    "dbatrade_name",
    "business_category",
    "dcwp_license_number",
    "inspection_type",
    "inspection_status",
    "noh_number",
    "address_type",
    "building_no",
    "street_name",
    "street_name_2",
    "unit_type",
    "unit",
    "city",
    "state",
    "postcode",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "nta",
    "latitude",
    "longitude"
FROM "nyc-open-data-jzhd-m6uv"
