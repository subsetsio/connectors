-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_ar",
    "type",
    "nationality_ar",
    "nationality",
    "revenue_type_ar",
    "revenue_type",
    "revenue_basis_ar",
    "revenue_basis",
    "value"
FROM "qatar-planning-and-statistics-authority-revenues-of-current-activity-by-type-and-insurance-company-nationality-insurance-statistics"
