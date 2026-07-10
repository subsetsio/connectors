-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("periode" AS VARCHAR) AS "periode",
    CAST("abstimmungsvorlage_thema" AS VARCHAR) AS "abstimmungsvorlage_thema",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1703010000-103"
