-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State or location" AS state_or_location,
    "Total" AS total,
    "DHS" AS dhs,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "DOI" AS doi,
    "DOT" AS dot,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda
FROM "ncses-nsf21329-tab093"
