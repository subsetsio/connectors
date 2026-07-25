-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "agency",
    "city",
    "state",
    "ntd_id",
    "organization_type",
    "reporter_type",
    CAST("report_year" AS BIGINT) AS report_year,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    "modes",
    "facility_type",
    CAST("pre1940" AS BIGINT) AS pre1940,
    CAST("_1940s" AS BIGINT) AS 1940s,
    CAST("_1950s" AS BIGINT) AS 1950s,
    CAST("_1960s" AS BIGINT) AS 1960s,
    CAST("_1970s" AS BIGINT) AS 1970s,
    CAST("_1980s" AS BIGINT) AS 1980s,
    CAST("_1990s" AS BIGINT) AS 1990s,
    CAST("_2000s" AS BIGINT) AS 2000s,
    CAST("_2010s" AS BIGINT) AS 2010s,
    CAST("_2020s" AS BIGINT) AS 2020s,
    CAST("total_facilities" AS BIGINT) AS total_facilities
FROM "u-s-department-of-transportation-wfz2-eft6"
