-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_animals_and_birds",
    "no_of_animals_and_birds",
    "visitors"
FROM "qatar-planning-and-statistics-authority-type-of-animals-at-the-zoo-in-khor-park-garden-and-number-of-visitors"
