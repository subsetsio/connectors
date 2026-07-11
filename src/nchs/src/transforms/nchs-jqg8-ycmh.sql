-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "state",
    "statename",
    "raceethnicity",
    "sex",
    "agegroup",
    "year",
    "quarter",
    "yearquarter",
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "deaths_weighted",
    "covid19_weighted",
    "deaths_unweighted",
    "covid19_unweighted",
    "time_period",
    "average_number_of_deaths_weighted",
    "average_number_of_deaths_unweighted",
    "number_above_average_weighted",
    "percent_above_average_weighted",
    "number_above_average_unweighted",
    "percent_above_average_unweighted",
    "analysisdate",
    "suppression",
    "footnote",
    "type"
FROM "nchs-jqg8-ycmh"
