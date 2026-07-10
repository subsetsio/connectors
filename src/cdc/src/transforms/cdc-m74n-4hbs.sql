-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("AnalysisDate", '%m/%d/%Y')::DATE AS analysisdate,
    "Time Period" AS time_period,
    CAST("MMWRyear" AS BIGINT) AS mmwryear,
    CAST("MMWRweek" AS BIGINT) AS mmwrweek,
    strptime("Weekending", '%m/%d/%Y')::DATE AS weekending,
    "RaceEthnicity" AS raceethnicity,
    "Sex" AS sex,
    "AgeGroup" AS agegroup,
    CAST("Deaths (weighted)" AS BIGINT) AS deaths_weighted,
    CAST("COVID19 (weighted)" AS BIGINT) AS covid19_weighted,
    CAST("Deaths (unweighted)" AS BIGINT) AS deaths_unweighted,
    CAST("COVID19 (unweighted)" AS BIGINT) AS covid19_unweighted,
    CAST("Average number of deaths (weighted)" AS BIGINT) AS average_number_of_deaths_weighted,
    CAST("Average number of deaths (unweighted)" AS BIGINT) AS average_number_of_deaths_unweighted,
    CAST("Number above average (weighted)" AS BIGINT) AS number_above_average_weighted,
    CAST("Percent above average (weighted)" AS DOUBLE) AS percent_above_average_weighted,
    CAST("Number above average (unweighted)" AS BIGINT) AS number_above_average_unweighted,
    CAST("Percent above average (unweighted)" AS DOUBLE) AS percent_above_average_unweighted,
    "Footnote" AS footnote,
    "Geography" AS geography
FROM "cdc-m74n-4hbs"
