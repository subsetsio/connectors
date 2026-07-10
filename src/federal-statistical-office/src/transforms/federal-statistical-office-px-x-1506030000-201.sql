-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("fachbereich" AS VARCHAR) AS "fachbereich",
    CAST("aufwandsart" AS VARCHAR) AS "aufwandsart",
    CAST("finanzierungstyp" AS VARCHAR) AS "finanzierungstyp",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506030000-201"
