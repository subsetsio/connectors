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
FROM "qatar-planning-and-statistics-authority-monthly-distribution-of-live-broadcast-hours-of-the-general-program-of-al-kass-sport-channels-by"
