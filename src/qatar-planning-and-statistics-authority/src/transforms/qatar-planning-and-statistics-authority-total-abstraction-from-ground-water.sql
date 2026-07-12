-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ground_water_abstraction_mm3"
FROM "qatar-planning-and-statistics-authority-total-abstraction-from-ground-water"
