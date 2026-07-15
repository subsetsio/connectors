-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "centre_code",
    "centre_name",
    "license_issue_date",
    "license_tenure"
FROM "sg-data-d-aea5df8dc9e1850857afd0e5e8e25795"
