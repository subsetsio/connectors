-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "particulars_ar",
    "particulars",
    "revenue_item_ar",
    "revenue_item",
    "bank_nationality_ar",
    "bank_nationality",
    "value_qr_000"
FROM "qatar-planning-and-statistics-authority-revenues-of-current-activity-by-bank-nationality-banks-statistics"
