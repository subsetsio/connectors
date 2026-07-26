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
    "children_tested_for_lead_by_age_3_years_number",
    "children_tested_for_lead_by_age_3_years_number__notes" AS children_tested_for_lead_by_age_3_years_number_notes,
    "children_tested_for_lead_by_age_3_years_percentage",
    "children_tested_for_lead_by_age_3_years_percentage__notes" AS children_tested_for_lead_by_age_3_years_percentage_notes
FROM "nyc-open-data-fzh2-sxib"
