-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cause_of_the_accident",
    "cause_of_the_accident_ar",
    "death",
    "severe_injury",
    "slight_injury",
    "physical_damages"
FROM "qatar-planning-and-statistics-authority-number-of-cases-from-traffic-accidents-by-type-of-case-and-cause-of-the-accident"
