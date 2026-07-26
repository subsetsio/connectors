-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "case_year",
    "case_number",
    "incident_datetime",
    "borough",
    "battalion",
    "community_district",
    "precinct",
    "incident_classification",
    "cause_fire_description",
    "fire_code_category"
FROM "nyc-open-data-ii3r-svjz"
