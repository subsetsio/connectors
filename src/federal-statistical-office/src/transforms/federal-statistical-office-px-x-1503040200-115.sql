-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("examensstufe" AS VARCHAR) AS "examensstufe",
    CAST("fachbereich" AS VARCHAR) AS "fachbereich",
    CAST("bildungsherkunft" AS VARCHAR) AS "bildungsherkunft",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503040200-115"
