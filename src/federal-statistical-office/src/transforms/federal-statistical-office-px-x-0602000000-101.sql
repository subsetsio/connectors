-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("economic_division" AS VARCHAR) AS "economic_division",
    CAST("employment_rate" AS VARCHAR) AS "employment_rate",
    CAST("gender" AS VARCHAR) AS "gender",
    CAST("quarter" AS VARCHAR) AS "quarter",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0602000000-101"
