-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gem_plant_id",
    "gem_unit_id",
    "unit_name",
    "gem_wiki_page",
    "country_area",
    "unit_status",
    "announced_date",
    "construction_date",
    "start_date",
    "unit_age",
    "pre_retirement_announcement_date",
    "idled_date",
    "retired_date",
    "furnace_manufacturer",
    "furnace_model",
    "current_capacity_ttpa",
    "current_size_tonnes",
    "scrap_based",
    "scrap",
    "dri",
    "hbi",
    "sponge_iron_unknown_if_dri_or_hbi",
    "basic_merchant_pig_iron",
    "granulated_pig_iron",
    "pig_iron_unknown_if_basic_merchant_or_granulated",
    "other_iron",
    "known_total"
FROM "gem-global-energy-monitor-iron-steel-steel-unit"
