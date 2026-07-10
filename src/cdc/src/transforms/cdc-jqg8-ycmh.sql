-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "StateName" AS statename,
    "RaceEthnicity" AS raceethnicity,
    "Sex" AS sex,
    "AgeGroup" AS agegroup,
    CAST("Year" AS BIGINT) AS year,
    "Quarter" AS quarter,
    "YearQuarter" AS yearquarter,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    CAST("Deaths (weighted)" AS BIGINT) AS deaths_weighted,
    CAST("COVID19 (weighted)" AS BIGINT) AS covid19_weighted,
    CAST("Deaths (unweighted)" AS BIGINT) AS deaths_unweighted,
    CAST("COVID19 (unweighted)" AS BIGINT) AS covid19_unweighted,
    "Time Period" AS time_period,
    CAST("Average number of deaths (weighted)" AS BIGINT) AS average_number_of_deaths_weighted,
    CAST("Average number of deaths (unweighted)" AS BIGINT) AS average_number_of_deaths_unweighted,
    CAST("Number above average (weighted)" AS BIGINT) AS number_above_average_weighted,
    CAST("Percent above average (weighted)" AS DOUBLE) AS percent_above_average_weighted,
    CAST("Number above average (unweighted)" AS BIGINT) AS number_above_average_unweighted,
    CAST("Percent above average (unweighted)" AS DOUBLE) AS percent_above_average_unweighted,
    "AnalysisDate" AS analysisdate,
    "Suppression" AS suppression,
    "Footnote" AS footnote,
    "Type" AS type
FROM "cdc-jqg8-ycmh"
