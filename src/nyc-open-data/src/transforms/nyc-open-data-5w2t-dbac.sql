-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "awarding_agency",
    "contract_identification_number",
    "mwbe_status",
    "purpose",
    "vendor_name",
    "zip_code",
    "original_start_date",
    "original_end_date",
    "start_date",
    "end_date",
    "registration_date",
    "last_modified_date",
    "original_contract_amount",
    "covid_encumbered_amount",
    "covid_spend_to_date",
    "funding_type",
    "award_method",
    "contract_type",
    "subcontractors"
FROM "nyc-open-data-5w2t-dbac"
