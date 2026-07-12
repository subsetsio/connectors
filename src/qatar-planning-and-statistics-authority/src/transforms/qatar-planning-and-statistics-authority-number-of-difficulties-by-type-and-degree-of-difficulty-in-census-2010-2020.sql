-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_difficulty",
    "level_of_difficulty",
    "percentage_of_change_from_2010_to_2020",
    "percentage_of_population_in_2020",
    "population_in_2020",
    "percentage_of_population_in_2010",
    "population_in_2010"
FROM "qatar-planning-and-statistics-authority-number-of-difficulties-by-type-and-degree-of-difficulty-in-census-2010-2020"
