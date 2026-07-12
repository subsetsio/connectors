-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "animal_type",
    "animal_type_ar",
    "species_count",
    "animal_count"
FROM "qatar-planning-and-statistics-authority-type-classification-of-animals-at-the-zoo-in-khor-park-2024"
