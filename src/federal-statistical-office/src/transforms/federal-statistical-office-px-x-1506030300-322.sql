-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("source_de_financement" AS VARCHAR) AS "source_de_financement",
    CAST("haute_école" AS VARCHAR) AS "haute_école",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506030300-322"
