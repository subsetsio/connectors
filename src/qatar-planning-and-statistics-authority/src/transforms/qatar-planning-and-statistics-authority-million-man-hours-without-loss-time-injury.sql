-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "million_man_hours"
FROM "qatar-planning-and-statistics-authority-million-man-hours-without-loss-time-injury"
