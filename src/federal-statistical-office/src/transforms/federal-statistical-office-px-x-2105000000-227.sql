-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("stadt_agglomeration" AS VARCHAR) AS "stadt_agglomeration",
    CAST("indikator" AS VARCHAR) AS "indikator",
    CAST("absolut_relativ" AS VARCHAR) AS "absolut_relativ",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-2105000000-227"
