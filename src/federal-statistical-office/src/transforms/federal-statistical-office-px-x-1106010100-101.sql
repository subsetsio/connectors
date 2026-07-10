-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("gravité_de_l_accident" AS VARCHAR) AS "gravité_de_l_accident",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("genre_de_route" AS VARCHAR) AS "genre_de_route",
    CAST("lieu_de_l_accident" AS VARCHAR) AS "lieu_de_l_accident",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1106010100-101"
