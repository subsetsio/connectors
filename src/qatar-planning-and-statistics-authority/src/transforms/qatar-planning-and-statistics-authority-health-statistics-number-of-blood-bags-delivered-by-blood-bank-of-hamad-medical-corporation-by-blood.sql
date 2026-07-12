-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "a",
    "a0",
    "ab",
    "ab0",
    "b",
    "b0",
    "o",
    "o0",
    "rare_blood_group"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-blood-bags-delivered-by-blood-bank-of-hamad-medical-corporation-by-blood"
