-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field medical school space and research animal space" AS field_medical_school_space_and_research_animal_space,
    "FY 2007" AS fy_2007,
    "FY 2009" AS fy_2009,
    "FY 2011" AS fy_2011,
    "FY 2013" AS fy_2013,
    "FY 2015" AS fy_2015,
    "FY 2017" AS fy_2017,
    "FY 2019" AS fy_2019,
    "FY 2021" AS fy_2021,
    "FY 2023" AS fy_2023
FROM "ncses-nsf25319-tab001"
