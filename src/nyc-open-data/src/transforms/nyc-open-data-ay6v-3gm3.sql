-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borough",
    "submitted_applications_for_benefits_under_snap",
    "received_benefits_under_snap",
    "were_incomeeligible_for_snap_benefits",
    "submitted_applications_for_benefits_under_cash_assistance",
    "received_benefits_under_cash_assistance",
    "were_incomeeligible_for_cash_assisstance"
FROM "nyc-open-data-ay6v-3gm3"
