-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "educational_status_of_mother",
    "lhl_lt_lymy_ll_m",
    "educational_status_of_father",
    "lhl_lt_lymy_ll_b",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-educational-status-of-father-and-mother-foreigners"
