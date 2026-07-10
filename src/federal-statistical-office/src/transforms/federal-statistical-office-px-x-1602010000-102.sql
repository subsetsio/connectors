-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("country_of_origin" AS VARCHAR) AS "country_of_origin",
    CAST("all_films_new_releases" AS VARCHAR) AS "all_films_new_releases",
    CAST("observation_unit" AS VARCHAR) AS "observation_unit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1602010000-102"
