-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("fachbereich" AS VARCHAR) AS "fachbereich",
    CAST("leistung" AS VARCHAR) AS "leistung",
    CAST("erlöskategorie" AS VARCHAR) AS "erlöskategorie",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506030100-204"
