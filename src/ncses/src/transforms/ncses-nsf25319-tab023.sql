-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of institution" AS type_of_institution,
    "All institutions number" AS all_institutions_number,
    "Institutions with repair and renovation projects - Number" AS institutions_with_repair_and_renovation_projects_number,
    "Institutions with repair and renovation projects - Percent" AS institutions_with_repair_and_renovation_projects_percent,
    "Institutions with new construction projects - Number" AS institutions_with_new_construction_projects_number,
    "Institutions with new construction projects - Percent" AS institutions_with_new_construction_projects_percent
FROM "ncses-nsf25319-tab023"
