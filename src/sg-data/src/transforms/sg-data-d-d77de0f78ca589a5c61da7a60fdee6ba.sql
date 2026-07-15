-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "reg_no",
    "firm_name",
    "firm_address",
    "firm_phone"
FROM "sg-data-d-d77de0f78ca589a5c61da7a60fdee6ba"
