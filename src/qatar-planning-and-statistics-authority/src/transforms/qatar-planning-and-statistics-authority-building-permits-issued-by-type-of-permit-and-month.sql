-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "permit_type",
    "nw_lrkhs",
    "count"
FROM "qatar-planning-and-statistics-authority-building-permits-issued-by-type-of-permit-and-month"
