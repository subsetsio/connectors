-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "year",
    "education_level",
    "race_or_hispanic_origin",
    "sex",
    "age_group",
    "total_deaths",
    "covid_19_deaths"
FROM "nchs-4ueh-89p9"
