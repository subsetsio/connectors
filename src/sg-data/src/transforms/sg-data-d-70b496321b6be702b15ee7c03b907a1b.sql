-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "salutation",
    "name",
    "designation",
    "organisation",
    "email_address",
    "area_of_expertise"
FROM "sg-data-d-70b496321b6be702b15ee7c03b907a1b"
