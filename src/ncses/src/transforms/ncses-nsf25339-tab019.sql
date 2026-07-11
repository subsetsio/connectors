-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "All agencies" AS all_agencies,
    "DOC" AS doc,
    "DODa" AS doda,
    "DOE" AS doe,
    "ED" AS ed,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda,
    "Otherb" AS otherb
FROM "ncses-nsf25339-tab019"
