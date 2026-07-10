-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unit_of_measure" AS VARCHAR) AS "unit_of_measure",
    CAST("economy_and_households" AS VARCHAR) AS "economy_and_households",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0204000000-104"
