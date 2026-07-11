-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State outlying area and institution" AS state_outlying_area_and_institution,
    "All agencies" AS all_agencies,
    "DOD" AS dod,
    "DOE" AS doe,
    "DOT" AS dot,
    "HHS" AS hhs,
    "NSF" AS nsf
FROM "ncses-nsf25339-tab016"
