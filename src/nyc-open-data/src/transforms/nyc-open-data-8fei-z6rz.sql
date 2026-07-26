-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_of_inspection",
    "inspection_number",
    "date_of_occurance",
    "business_unique_id",
    "business_name",
    "dba_trade_name",
    "business_category",
    "inspection_type",
    "device_category",
    "device_class",
    "device_type",
    "devices_inspected",
    "devices_approved",
    "devices_condemnedconfiscated",
    "address_type",
    "building_number",
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
FROM "nyc-open-data-8fei-z6rz"
