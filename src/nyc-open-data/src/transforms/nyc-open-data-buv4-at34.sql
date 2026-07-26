-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "awarding_agency",
    "recipient_name",
    "service_type",
    "recipient_zip_code",
    "recipient_description",
    "funding_source",
    "loangrant_number",
    "loangrant_amount",
    "funded_date",
    "maturity_date",
    "purpose"
FROM "nyc-open-data-buv4-at34"
