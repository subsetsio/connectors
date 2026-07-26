-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "business_name",
    "business_category",
    "business_unique_id",
    "dbatrade_name",
    "asset_type",
    "business_asset_id",
    "manufacture_identification_number",
    "dmv_license_plate_number",
    "state_of_registration",
    "dcwp_plate_number",
    "decal_number",
    "latest_inspection_number",
    "latest_inspection_date",
    "latest_inspection_result"
FROM "nyc-open-data-9vpn-rpgs"
