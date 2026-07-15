-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_quarter",
    "usages",
    "estimated_gfa"
FROM "sg-data-d-e89cd21c636e5b7588b73cec0090de00"
