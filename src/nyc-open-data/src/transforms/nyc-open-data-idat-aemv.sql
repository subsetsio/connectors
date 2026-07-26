-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "gender",
    "race",
    "ethnicity",
    "marital_status",
    "gross_monthly_income",
    "military_affiliation",
    "current_status",
    "branch",
    "service_era",
    "discharge_type",
    "current_client_address_postal_code"
FROM "nyc-open-data-idat-aemv"
