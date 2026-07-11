-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FFRDC" AS ffrdc,
    "Total" AS total,
    "DHS" AS dhs,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "Othera" AS othera
FROM "ncses-nsf21329-tab013"
