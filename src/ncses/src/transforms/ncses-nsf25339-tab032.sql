-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State outlying area and institution" AS state_outlying_area_and_institution,
    "All agencies" AS all_agencies,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "DOI" AS doi,
    "ED" AS ed,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda,
    "Othera" AS othera
FROM "ncses-nsf25339-tab032"
