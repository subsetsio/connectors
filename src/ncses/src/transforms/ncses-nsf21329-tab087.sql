-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Region country or economy" AS region_country_or_economy,
    "Total" AS total,
    "DOC" AS doc,
    "DOD" AS dod,
    "DOE" AS doe,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NSF" AS nsf,
    "USDA" AS usda
FROM "ncses-nsf21329-tab087"
