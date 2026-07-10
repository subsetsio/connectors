-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are date by lower-tier local authority observations; national or regional totals require grouping by the intended geography level.
SELECT
    "date",
    "areaName" AS areaname,
    "Region" AS region,
    CAST("Confirmed Omicron cases" AS BIGINT) AS confirmed_omicron_cases,
    CAST("SGTF cases" AS BIGINT) AS sgtf_cases,
    CAST("Total" AS BIGINT) AS total,
    CAST("newCasesBySpecimenDate" AS DOUBLE) AS newcasesbyspecimendate,
    CAST("long" AS DOUBLE) AS long,
    CAST("lat" AS DOUBLE) AS lat
FROM "global-health-omicron-uk-ltla"
