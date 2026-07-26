-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider_first_name",
    "provider_last_name",
    "practice_name",
    "primary_speciality",
    "site_name",
    "practice_borough",
    "practice_mailing_address",
    "organization_type",
    "practice_zip_code"
FROM "nyc-open-data-7btz-mnc8"
