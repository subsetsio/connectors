-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unit_of_measure" AS VARCHAR) AS "unit_of_measure",
    CAST("environmental_domain" AS VARCHAR) AS "environmental_domain",
    CAST("economic_activity" AS VARCHAR) AS "economic_activity",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0204000000-111"
