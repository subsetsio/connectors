-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Consortium" AS consortium,
    "All agencies" AS all_agencies,
    "DHS" AS dhs,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "DOT" AS dot,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda
FROM "ncses-nsf25339-tab037"
