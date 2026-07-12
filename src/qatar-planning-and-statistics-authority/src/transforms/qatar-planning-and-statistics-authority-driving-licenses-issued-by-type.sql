-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "license_type",
    "nw_lrkhs",
    "issuance_type",
    "nw_lsdr",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-driving-licenses-issued-by-type"
