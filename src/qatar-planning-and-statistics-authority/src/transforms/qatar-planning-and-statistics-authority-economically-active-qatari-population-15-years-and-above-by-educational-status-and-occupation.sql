-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation",
    "lmhn",
    "educational_status",
    "lhl_lt_lymy",
    "total"
FROM "qatar-planning-and-statistics-authority-economically-active-qatari-population-15-years-and-above-by-educational-status-and-occupation"
