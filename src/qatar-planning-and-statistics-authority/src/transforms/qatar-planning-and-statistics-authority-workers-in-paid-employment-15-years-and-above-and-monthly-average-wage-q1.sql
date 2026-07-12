-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "lnw",
    "occupation",
    "lmhn",
    "paid_employment_workers",
    "monthly_average_wage_qr"
FROM "qatar-planning-and-statistics-authority-workers-in-paid-employment-15-years-and-above-and-monthly-average-wage-q1"
