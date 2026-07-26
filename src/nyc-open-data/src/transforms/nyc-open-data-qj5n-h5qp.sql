-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "managing_agency",
    "fms_id",
    "yearmonth_reported",
    "total_budget",
    "spend_to_date",
    "spend_to_date_1",
    "budget_variance",
    "budget_variance_1"
FROM "nyc-open-data-qj5n-h5qp"
