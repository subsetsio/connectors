-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency",
    "industry",
    "count",
    "contract_value",
    "percent_awarded_to_worker_coops"
FROM "nyc-open-data-aejp-3ws7"
