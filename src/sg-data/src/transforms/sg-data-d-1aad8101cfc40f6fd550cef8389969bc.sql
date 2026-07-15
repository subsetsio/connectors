-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "module_type",
    "participant_category",
    "fee_per_module"
FROM "sg-data-d-1aad8101cfc40f6fd550cef8389969bc"
