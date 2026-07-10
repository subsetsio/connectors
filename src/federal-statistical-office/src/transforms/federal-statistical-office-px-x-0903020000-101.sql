-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("nombre_de_pièces" AS VARCHAR) AS "nombre_de_pièces",
    CAST("mode_d_utilisation_du_logement" AS VARCHAR) AS "mode_d_utilisation_du_logement",
    CAST("statut_d_occupation" AS VARCHAR) AS "statut_d_occupation",
    CAST("loyer_mensuel_net" AS VARCHAR) AS "loyer_mensuel_net",
    CAST("surface_du_logement" AS VARCHAR) AS "surface_du_logement",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0903020000-101"
