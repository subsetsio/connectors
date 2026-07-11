-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field medical school space and research animal space" AS field_medical_school_space_and_research_animal_space,
    "All institutions" AS all_institutions,
    "Doctorate granting - All" AS doctorate_granting_all,
    "Doctorate granting - Public" AS doctorate_granting_public,
    "Doctorate granting - Private" AS doctorate_granting_private,
    "Nondoctorate granting - Private" AS nondoctorate_granting_private
FROM "ncses-nsf25319-tab002"
