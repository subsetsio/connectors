-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("major_region" AS VARCHAR) AS "major_region",
    CAST("employment_prospects" AS VARCHAR) AS "employment_prospects",
    CAST("weight" AS VARCHAR) AS "weight",
    CAST("quarter" AS VARCHAR) AS "quarter",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0602000000-106"
