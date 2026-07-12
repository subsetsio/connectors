-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "duration_of_employment_search_in_months",
    "value"
FROM "qatar-planning-and-statistics-authority-unemployed-15-years-and-above-by-nationality-gender-and-duration-of-employment-search-in-months"
