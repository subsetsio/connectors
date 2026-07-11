-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State and outlying area" AS state_and_outlying_area,
    "All agencies" AS all_agencies,
    "DOC" AS doc,
    "DOT" AS dot,
    "ED" AS ed,
    "HHS" AS hhs,
    "NSF" AS nsf,
    "USDA" AS usda
FROM "ncses-nsf25339-tab011"
