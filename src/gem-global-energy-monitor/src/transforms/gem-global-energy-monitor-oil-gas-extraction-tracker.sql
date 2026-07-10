-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unit_id",
    "unit_name",
    "unit_name_local_script",
    "fuel_type",
    "country_area",
    "subnational_unit",
    "production_type",
    "status",
    "status_detail",
    "status_year",
    "discovery_year",
    "fid_year",
    "production_start_year",
    "operator",
    "owner_s",
    "parent_s",
    "government_unit_id",
    "wiki_url_project",
    "wiki_url_field",
    "name_other",
    "latitude",
    "longitude",
    "location_accuracy",
    "onshore_offshore",
    "field_outline_wkt",
    "basin",
    "block_s"
FROM "gem-global-energy-monitor-oil-gas-extraction-tracker"
