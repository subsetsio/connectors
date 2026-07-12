-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_types_of_animals_and_birds",
    "no_of_animals_and_birds",
    "visitors_in_thousands"
FROM "qatar-planning-and-statistics-authority-media-culture-and-tourism-statistics-number-of-types-of-animals-at-the-zoological-garden-and-number"
