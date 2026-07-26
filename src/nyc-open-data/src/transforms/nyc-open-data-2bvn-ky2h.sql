-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "contract_id",
    "contract_number",
    "start_date",
    "end_date",
    "amount",
    "fiscal_year",
    "purpose",
    "program_id",
    "provider_id",
    "agency_name"
FROM "nyc-open-data-2bvn-ky2h"
