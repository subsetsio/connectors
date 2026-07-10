-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("type_de_bâtiment" AS VARCHAR) AS "type_de_bâtiment",
    CAST("type_de_propriétaire" AS VARCHAR) AS "type_de_propriétaire",
    CAST("propriété_par_étage" AS VARCHAR) AS "propriété_par_étage",
    CAST("epoque_de_construction" AS VARCHAR) AS "epoque_de_construction",
    CAST("nombre_d_étages" AS VARCHAR) AS "nombre_d_étages",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-113"
