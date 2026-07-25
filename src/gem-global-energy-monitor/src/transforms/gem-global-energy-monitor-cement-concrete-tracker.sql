-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gem_plant_id",
    "gem_asset_name_english",
    "asset_name_other_language",
    "alternative_asset_name_s",
    "sfi_id",
    "leadit_project_id",
    "coordinates",
    "coordinate_accuracy",
    "gem_wiki_page",
    "municipality",
    "subnational_unit",
    "country_area",
    "cement_capacity_millions_metric_tonnes_per_annum",
    "clinker_capacity_millions_metric_tonnes_per_annum",
    "majority_cement_type",
    "cement_color",
    "operating_status",
    "start_date",
    "owner_name_english",
    "owner_name_other_language",
    "owner_entity_id",
    "parent",
    "parent_entity_id",
    "plant_type",
    "production_type",
    "ccs_ccus",
    "alternative_fuel",
    "clay_calcination"
FROM "gem-global-energy-monitor-cement-concrete-tracker"
