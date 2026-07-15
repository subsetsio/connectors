-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "firm_name",
    "firm_address",
    "firm_phone",
    "firm_fax",
    "firm_email"
FROM "sg-data-d-d5c0a4ffd076a3e40d772275619bbb66"
