-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "centre_code",
    "centre_name",
    "incidental_charges",
    "frequency",
    "amount"
FROM "sg-data-d-253a7e348279bf0a87666a71f7ea2e67"
