-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "state",
    "race_hispanic_origin",
    "count_of_covid_19_deaths",
    "distribution_of_covid_19_deaths",
    "unweighted_distribution_of_population",
    "weighted_distribution_of_population",
    "difference_between_covid_19_and_unweighted_population",
    "difference_between_covid_19_and_weighted_population",
    "agegroup",
    "suppression"
FROM "nchs-jwta-jxbg"
