-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_code",
    "tax_block",
    "tax_lot",
    "bbl",
    "zoning_district_1",
    "zoning_district_2",
    "zoning_district_3",
    "zoning_district_4",
    "commercial_overlay_1",
    "commercial_overlay_2",
    "special_district_1",
    "special_district_2",
    "special_district_3",
    "limited_height_district",
    "zoning_map_number",
    "zoning_map_code"
FROM "nyc-open-data-fdkv-4t4z"
