-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("gemeinde" AS VARCHAR) AS "gemeinde",
    CAST("gebäudekategorie" AS VARCHAR) AS "gebäudekategorie",
    CAST("bauperiode" AS VARCHAR) AS "bauperiode",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-107"
