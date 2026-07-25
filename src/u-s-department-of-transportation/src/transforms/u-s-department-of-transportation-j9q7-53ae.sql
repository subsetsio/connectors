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
    "mode",
    "mode_name",
    "type_of_service",
    "guideway_element",
    CAST("pre1940s" AS DOUBLE) AS pre1940s,
    "pre1940s_q",
    CAST("_1940s" AS DOUBLE) AS 1940s,
    "_1940s_q" AS 1940s_q,
    CAST("_1950s" AS DOUBLE) AS 1950s,
    "_1950s_q" AS 1950s_q,
    CAST("_1960s" AS DOUBLE) AS 1960s,
    "_1960s_q" AS 1960s_q,
    CAST("_1970s" AS DOUBLE) AS 1970s,
    "_1970s_q" AS 1970s_q,
    CAST("_1980s" AS DOUBLE) AS 1980s,
    "_1980s_q" AS 1980s_q,
    CAST("_1990s" AS DOUBLE) AS 1990s,
    "_1990s_q" AS 1990s_q,
    CAST("_2000s" AS DOUBLE) AS 2000s,
    "_2000s_q" AS 2000s_q,
    CAST("_2010s" AS DOUBLE) AS 2010s,
    "_2010s_q" AS 2010s_q,
    CAST("_2020s" AS DOUBLE) AS 2020s,
    "_2020s_q" AS 2020s_q
FROM "u-s-department-of-transportation-j9q7-53ae"
