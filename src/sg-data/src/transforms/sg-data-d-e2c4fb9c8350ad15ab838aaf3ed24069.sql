-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "discharge_date",
    "bankruptcy_no"
FROM "sg-data-d-e2c4fb9c8350ad15ab838aaf3ed24069"
