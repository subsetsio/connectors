-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "State" AS state,
    "Race/Hispanic origin" AS race_hispanic_origin,
    CAST("Count of COVID-19 deaths" AS BIGINT) AS count_of_covid_19_deaths,
    CAST("Distribution of COVID-19 deaths (%)" AS DOUBLE) AS distribution_of_covid_19_deaths,
    CAST("Unweighted distribution of population (%)" AS DOUBLE) AS unweighted_distribution_of_population,
    CAST("Weighted distribution of population (%)" AS DOUBLE) AS weighted_distribution_of_population,
    CAST("Difference between COVID-19 and unweighted population %" AS DOUBLE) AS difference_between_covid_19_and_unweighted_population,
    CAST("Difference between COVID-19 and weighted population %" AS DOUBLE) AS difference_between_covid_19_and_weighted_population,
    "AgeGroup" AS agegroup,
    "Suppression" AS suppression
FROM "cdc-jwta-jxbg"
