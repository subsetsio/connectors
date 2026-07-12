-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "program_type",
    "nw_lbrnmj",
    "hours"
FROM "qatar-planning-and-statistics-authority-television-programs-and-the-number-of-hours-broadcast-of-the-qatar-tv"
