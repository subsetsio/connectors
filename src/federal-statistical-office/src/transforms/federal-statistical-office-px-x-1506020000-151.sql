-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506020000-151"
