-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gem_plant_id",
    "plant_name_english",
    "plant_name_other_language",
    "other_plant_names_english",
    "other_plant_names_other_language",
    "sfi_id",
    "owner_english",
    "owner_other_language",
    "owner_gem_entity_id",
    "municipality",
    "subnational_unit",
    "country_area",
    "region",
    "iso3_code",
    "coordinates",
    "coordinate_accuracy",
    "gem_wiki_page",
    "primary_products",
    "secondary_products",
    "feedstock",
    "feedstock_accuracy"
FROM "gem-global-energy-monitor-chemicals-inventory"
