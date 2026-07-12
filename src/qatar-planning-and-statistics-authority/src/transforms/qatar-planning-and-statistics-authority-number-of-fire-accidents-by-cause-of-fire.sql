-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cause_of_fire",
    "number_of_fire_accidents",
    "cause_of_fire_ar"
FROM "qatar-planning-and-statistics-authority-number-of-fire-accidents-by-cause-of-fire"
