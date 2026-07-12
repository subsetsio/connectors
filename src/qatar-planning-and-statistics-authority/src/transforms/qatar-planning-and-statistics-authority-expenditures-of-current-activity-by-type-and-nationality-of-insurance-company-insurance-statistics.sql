-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnw",
    "type",
    "ljnsy",
    "nationality",
    "nw_lm_ml",
    "transaction_type",
    "ss_lm_ml",
    "transaction_basis",
    "value"
FROM "qatar-planning-and-statistics-authority-expenditures-of-current-activity-by-type-and-nationality-of-insurance-company-insurance-statistics"
