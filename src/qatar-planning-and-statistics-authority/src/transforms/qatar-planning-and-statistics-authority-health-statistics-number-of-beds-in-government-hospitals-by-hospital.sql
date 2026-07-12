-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "hospital",
    "hospital_ar",
    "number_of_beds_dd_l_sr"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-beds-in-government-hospitals-by-hospital"
