-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("AnalysisDate", '%m/%d/%Y')::DATE AS analysisdate,
    "HHS Region" AS hhs_region,
    "RaceEthnicity" AS raceethnicity,
    "AgeGroup" AS agegroup,
    CAST("MMWRyear" AS BIGINT) AS mmwryear,
    CAST("MMWRweek" AS BIGINT) AS mmwrweek,
    strptime("WeekEndingDate", '%m/%d/%Y')::DATE AS weekendingdate,
    CAST("AllCause" AS BIGINT) AS allcause,
    CAST("COVID-19 (U071, Multiple Cause of Death)" AS BIGINT) AS covid_19_u071_multiple_cause_of_death,
    CAST("COVID-19 (U071,Underlying Cause of Death)" AS BIGINT) AS covid_19_u071_underlying_cause_of_death,
    "flag_allcause",
    "flag_covidmcod",
    "flag_coviducod"
FROM "cdc-xy7w-35q7"
