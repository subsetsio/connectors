-- Statistics Canada table 34-10-0128 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
SELECT
    CAST("REF_DATE" AS BIGINT) AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100128"
WHERE "VALUE" IS NOT NULL
