-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "substance",
    "lmd",
    "global_warming_potential_gwp_100_years",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024"
FROM "qatar-planning-and-statistics-authority-ozone-depleting-potential-by-substance-and-ghg-potential-tons-co2-equivalents"
