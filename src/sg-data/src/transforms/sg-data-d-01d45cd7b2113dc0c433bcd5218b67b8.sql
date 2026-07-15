-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Diseases" AS diseases
FROM "sg-data-d-01d45cd7b2113dc0c433bcd5218b67b8"
