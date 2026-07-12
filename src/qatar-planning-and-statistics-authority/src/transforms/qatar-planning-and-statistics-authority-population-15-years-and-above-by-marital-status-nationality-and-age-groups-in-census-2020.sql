-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "ljnsy",
    "age_group",
    "never_married_population",
    "never_married",
    "married_population",
    "married",
    "divorced_population",
    "divorced",
    "widowed_population",
    "widowed"
FROM "qatar-planning-and-statistics-authority-population-15-years-and-above-by-marital-status-nationality-and-age-groups-in-census-2020"
