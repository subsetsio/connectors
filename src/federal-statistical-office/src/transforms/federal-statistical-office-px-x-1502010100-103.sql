-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("schulkanton" AS VARCHAR) AS "schulkanton",
    CAST("unterrichtsart" AS VARCHAR) AS "unterrichtsart",
    CAST("lehrplananpassungen" AS VARCHAR) AS "lehrplananpassungen",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502010100-103"
