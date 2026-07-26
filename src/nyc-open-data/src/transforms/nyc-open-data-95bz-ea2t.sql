-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "pension_systems",
    "fiscal_year",
    "pension_expenses"
FROM "nyc-open-data-95bz-ea2t"
