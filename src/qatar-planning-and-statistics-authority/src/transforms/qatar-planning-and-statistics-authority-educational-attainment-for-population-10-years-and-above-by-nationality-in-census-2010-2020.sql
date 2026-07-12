-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "educational_attainment",
    "educational_attainment_ar",
    "2010_population",
    "percentage_of_2010_population",
    "2020_population",
    "precentage_of_2020_population",
    "change_precentage"
FROM "qatar-planning-and-statistics-authority-educational-attainment-for-population-10-years-and-above-by-nationality-in-census-2010-2020"
