-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("analysisdate", '%m/%d/%Y')::DATE AS analysisdate,
    "time_period",
    "mmwryear",
    "mmwrweek",
    strptime("weekending", '%m/%d/%Y')::DATE AS weekending,
    "raceethnicity",
    "sex",
    "agegroup",
    "deaths_weighted",
    "covid19_weighted",
    "deaths_unweighted",
    "covid19_unweighted",
    "average_number_of_deaths_weighted",
    "average_number_of_deaths_unweighted",
    "number_above_average_weighted",
    "percent_above_average_weighted",
    "number_above_average_unweighted",
    "percent_above_average_unweighted",
    "footnote",
    "geography"
FROM "nchs-m74n-4hbs"
