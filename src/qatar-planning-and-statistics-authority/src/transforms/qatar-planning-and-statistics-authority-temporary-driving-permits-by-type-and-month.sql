-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "permit_type",
    "nw_ltsryh",
    "issuance_type",
    "nw_lsdr",
    "number"
FROM "qatar-planning-and-statistics-authority-temporary-driving-permits-by-type-and-month"
