-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual adjustment factor rows mix metropolitan, county, and nonmetropolitan HUD area definitions; filter to the intended area coding before comparing or aggregating areas.
SELECT
    "northeast_region",
    "col_1",
    "1_024950915508538",
    "1_0204239093699472",
    "1_029",
    "1_024",
    "1_021648148503259",
    "1_0279111523444415",
    "region_cpi_metropolitan_area_name",
    "metropolitan_component_areas",
    "highest_cost_utility_included",
    "highest_cost_utility_excluded",
    "region_metropolitan_area_name",
    "fiscal_year"
FROM "hud-aaf"
