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
    "mw_shr",
    "indicator",
    "value"
FROM "qatar-planning-and-statistics-authority-number-and-value-of-insurance-policies-by-type-and-insurance-company-nationality-insurance"
