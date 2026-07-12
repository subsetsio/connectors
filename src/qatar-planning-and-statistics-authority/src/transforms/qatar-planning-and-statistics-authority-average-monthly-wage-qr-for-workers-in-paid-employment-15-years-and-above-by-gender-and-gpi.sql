-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "ljns",
    "gpi",
    "average"
FROM "qatar-planning-and-statistics-authority-average-monthly-wage-qr-for-workers-in-paid-employment-15-years-and-above-by-gender-and-gpi"
