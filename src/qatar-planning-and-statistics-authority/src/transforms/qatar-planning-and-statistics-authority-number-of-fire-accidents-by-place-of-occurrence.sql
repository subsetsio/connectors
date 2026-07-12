-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "place_of_occurrence",
    "number_of_fire_accidents",
    "place_of_occurrence_ar"
FROM "qatar-planning-and-statistics-authority-number-of-fire-accidents-by-place-of-occurrence"
