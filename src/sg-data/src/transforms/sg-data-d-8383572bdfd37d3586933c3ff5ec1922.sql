-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cleansvcpr",
    "email_add",
    "contact",
    "zone",
    "remark"
FROM "sg-data-d-8383572bdfd37d3586933c3ff5ec1922"
