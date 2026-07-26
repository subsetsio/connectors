-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_period",
    "managing_agency",
    "fms_id",
    "fiscal_year",
    "total_budget_city_non_city",
    "city",
    "non_city",
    "spend"
FROM "nyc-open-data-gyhf-rsr3"
