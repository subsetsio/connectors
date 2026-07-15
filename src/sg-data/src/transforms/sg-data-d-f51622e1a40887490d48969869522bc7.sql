-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "app_no",
    "licence_no",
    "company_name",
    "valid_period",
    "company_address",
    "tobacco_type_s"
FROM "sg-data-d-f51622e1a40887490d48969869522bc7"
