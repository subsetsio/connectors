-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "report_type",
    "metric",
    "demographic_type",
    "demographic_subtype",
    "number_of_applicants"
FROM "nyc-open-data-gcnt-k7eq"
