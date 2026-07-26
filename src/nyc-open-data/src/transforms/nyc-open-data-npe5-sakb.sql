-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "vendor",
    "purpose",
    "_method" AS method,
    "contract_value",
    "start_date",
    "end_date"
FROM "nyc-open-data-npe5-sakb"
