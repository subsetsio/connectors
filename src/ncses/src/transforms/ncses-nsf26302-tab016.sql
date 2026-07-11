-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Total federal" AS total_federal,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "DOI" AS doi,
    "DOT" AS dot,
    "ED" AS ed,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NSF" AS nsf,
    "USDA" AS usda,
    "Othera" AS othera
FROM "ncses-nsf26302-tab016"
