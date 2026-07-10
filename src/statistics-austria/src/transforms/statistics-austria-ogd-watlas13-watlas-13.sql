-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_1995" AS BIGINT) AS year_starting_1995,
    "federal_provinces",
    "agricultural_and_forestry_holdings",
    "labour_force_in_agricultural_holdings_in_total",
    "family_labour_force",
    "non_family_labour_force",
    "utilised_agricultural_area_uaa",
    "untilised_forestry_area_ha",
    "other_areas_ha",
    "arable_land_ha",
    "permanent_grassland_for_intensive_production_ha",
    "permanent_grassland_for_extensive_production_ha",
    "permanent_crops_ha",
    "kitchen_gardens_ha",
    "bovine_animals",
    "pigs",
    "sheep",
    "goats",
    "poultry"
FROM "statistics-austria-ogd-watlas13-watlas-13"
