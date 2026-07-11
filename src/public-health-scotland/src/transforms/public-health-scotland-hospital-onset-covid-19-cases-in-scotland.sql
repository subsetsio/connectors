-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "Country" AS country,
    strptime("WeekEnding", '%Y%m%d')::DATE AS weekending,
    CAST("WeekNumber" AS BIGINT) AS weeknumber,
    CAST("ProbableHospitalOnsetCOVID19" AS BIGINT) AS probablehospitalonsetcovid19,
    CAST("DefiniteHospitalOnsetCOVID19" AS BIGINT) AS definitehospitalonsetcovid19
FROM "public-health-scotland-hospital-onset-covid-19-cases-in-scotland"
