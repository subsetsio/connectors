-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_anonymous_reporting_accidents",
    "number_of_reconciliation_accidents"
FROM "qatar-planning-and-statistics-authority-number-of-reconciliation-and-anonymous-reporting-accidents"
