-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("examensstufe" AS VARCHAR) AS "examensstufe",
    CAST("fachbereichsgruppe" AS VARCHAR) AS "fachbereichsgruppe",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503040100-104"
