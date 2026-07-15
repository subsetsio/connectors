-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "no_of_approvals"
FROM "sg-data-d-c2b211174c4e0f546b4d8e92c6aaf365"
