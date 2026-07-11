-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "All federal R and D expenditures" AS all_federal_r_and_d_expenditures,
    "DOD" AS dod,
    "DOE" AS doe,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda,
    "Othera" AS othera
FROM "ncses-nsf26304-tab018"
