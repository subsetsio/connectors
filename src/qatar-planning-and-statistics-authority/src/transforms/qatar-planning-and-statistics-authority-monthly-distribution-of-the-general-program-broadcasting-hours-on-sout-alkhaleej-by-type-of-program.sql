-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "program_type",
    "nw_lbrnmj",
    "hours",
    "minutes"
FROM "qatar-planning-and-statistics-authority-monthly-distribution-of-the-general-program-broadcasting-hours-on-sout-alkhaleej-by-type-of-program"
