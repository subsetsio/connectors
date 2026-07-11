-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FFRDC" AS ffrdc,
    "Total" AS total,
    "DOD" AS dod,
    "DOE" AS doe,
    "NASA" AS nasa
FROM "ncses-nsf21329-tab014"
