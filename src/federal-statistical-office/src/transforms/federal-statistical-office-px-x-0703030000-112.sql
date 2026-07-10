-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("forest_zone" AS VARCHAR) AS "forest_zone",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("type_of_owner" AS VARCHAR) AS "type_of_owner",
    CAST("wood_species" AS VARCHAR) AS "wood_species",
    CAST("observation_unit" AS VARCHAR) AS "observation_unit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0703030000-112"
