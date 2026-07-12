-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cause_of_the_accident_ar",
    "cause_of_the_accident",
    "cases_ar",
    "cases",
    "no_of_traffic_accidents"
FROM "qatar-planning-and-statistics-authority-traffic-accidents-by-cause-of-the-accident-and-cases"
