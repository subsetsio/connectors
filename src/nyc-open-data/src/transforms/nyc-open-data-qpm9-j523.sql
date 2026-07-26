-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "org_id",
    "org_name",
    "org_address",
    "org_address2",
    "org_city",
    "org_state",
    "org_zip",
    "boro_id",
    "org_phone",
    "org_fax",
    "org_website",
    "org_email",
    "org_boundary",
    "org_neighborhood",
    "org_year",
    "org_realestate",
    "org_blocks",
    "org_businesses"
FROM "nyc-open-data-qpm9-j523"
