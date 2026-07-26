-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "contract_id",
    "organization_id",
    "agency_id",
    "agency_name",
    "service_id",
    "contract_amount",
    "contract_end",
    "contract_start",
    "contract_number",
    "fiscal_year"
FROM "nyc-open-data-c5up-ki6j"
