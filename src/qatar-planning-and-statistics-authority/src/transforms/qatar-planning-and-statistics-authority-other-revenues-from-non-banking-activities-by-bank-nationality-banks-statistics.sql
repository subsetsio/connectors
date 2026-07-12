-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lbyn",
    "particulars",
    "jnsy_lbnk",
    "bank_nationality",
    "value"
FROM "qatar-planning-and-statistics-authority-other-revenues-from-non-banking-activities-by-bank-nationality-banks-statistics"
