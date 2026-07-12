-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality_ar",
    "nationality",
    "employment_status",
    "employment_status_ar",
    "2010_population",
    "2010_population_percentage",
    "2020_population",
    "2020_population_percentage",
    "change"
FROM "qatar-planning-and-statistics-authority-population-economically-active-15-years-and-above-by-nationality-and-employment-status-in-census"
