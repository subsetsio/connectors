-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "relation_to_workforce",
    "relation_to_workforce_ar",
    "nationality",
    "ljnsy",
    "percentage_of_change_from_2010_to_2020",
    "percentage_of_population_in_2020",
    "population_in_2020",
    "percentage_of_population_in_2010",
    "population_in_2010"
FROM "qatar-planning-and-statistics-authority-qatari-economically-inactive-15-years-and-above-by-sex-and-relation-to-workforce-in-census-2010-2020"
