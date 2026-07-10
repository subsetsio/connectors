-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gem_asset_id",
    "asset_name_english",
    "asset_name_other_language",
    "coordinates",
    "coordinate_accuracy",
    "municipality",
    "subnational_unit",
    "country_area",
    "region",
    "production_2024_ttpa",
    "production_2023_ttpa",
    "production_2022_ttpa",
    "design_capacity_ttpa",
    "total_reserves_proven_and_probable_thousand_metric_tonnes",
    "total_resource_inferred_indicated_and_measured_thousand_metric_tonnes",
    "operating_status",
    "start_date",
    "stop_date",
    "owner",
    "owner_gem_entity_id",
    "owner_name_in_local_language_script",
    "parent",
    "parent_gem_entity_id",
    "gem_wiki_page_url"
FROM "gem-global-energy-monitor-iron-ore-mines-tracker"
