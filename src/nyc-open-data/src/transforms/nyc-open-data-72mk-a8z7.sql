-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "ownership_structure_code",
    "organization_phone",
    "doing_business_start_date"
FROM "nyc-open-data-72mk-a8z7"
