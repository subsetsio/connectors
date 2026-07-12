-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_animal",
    "type_of_animal_ar",
    "number_of_species",
    "number_of_animals"
FROM "qatar-planning-and-statistics-authority-media-culture-and-tourism-number-of-animals-and-different-type-of-species-in-zoological-garden-by"
