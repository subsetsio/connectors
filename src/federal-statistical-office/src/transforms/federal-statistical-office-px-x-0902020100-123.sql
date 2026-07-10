-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("gebäudekategorie" AS VARCHAR) AS "gebäudekategorie",
    CAST("hauseigentümertyp" AS VARCHAR) AS "hauseigentümertyp",
    CAST("bauperiode" AS VARCHAR) AS "bauperiode",
    CAST("anzahl_geschosse" AS VARCHAR) AS "anzahl_geschosse",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-123"
