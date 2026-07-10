-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("fachbereich" AS VARCHAR) AS "fachbereich",
    CAST("leistung" AS VARCHAR) AS "leistung",
    CAST("kostenart" AS VARCHAR) AS "kostenart",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506030000-221"
