-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Males" AS males,
    "Females" AS females
FROM "sg-data-d-ddb7ada7ec7c5ac7bc0d1d3ca3fb600a"
