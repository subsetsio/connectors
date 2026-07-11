-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "All agencies" AS all_agencies,
    "DHS" AS dhs,
    "DOC" AS doc,
    "DODa" AS doda,
    "DOE" AS doe,
    "DOI" AS doi,
    "DOT" AS dot,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "SSA" AS ssa,
    "USDA" AS usda
FROM "ncses-nsf25339-tab025"
