-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_type",
    "geo_area_id",
    "geo_area_name",
    "borough_id",
    "time_period",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll_5_gdl",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll_5_gdl__notes" AS children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll_5_gdl_notes,
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll10_gdl",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll10_gdl__notes" AS children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll10_gdl_notes,
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll15_gdl",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll15_gdl__notes" AS children_under_6_years_with_elevated_blood_lead_levels_bll_number_bll15_gdl_notes,
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_tested",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_number_tested__notes" AS children_under_6_years_with_elevated_blood_lead_levels_bll_number_tested_notes,
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll5_gdl_per_1000_tested",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll5_gdl_per_1000_tested_notes",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll10_gdl_per_1000_tested",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll10_gdl_per_1000_tested_notes",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll15_gdl_per_1000_tested",
    "children_under_6_years_with_elevated_blood_lead_levels_bll_rate_bll15_gdl_per_1000_tested_notes"
FROM "nyc-open-data-tnry-kwh5"
