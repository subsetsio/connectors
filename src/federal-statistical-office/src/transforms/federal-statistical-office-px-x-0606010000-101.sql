-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("sitzland_auswahl" AS VARCHAR) AS "sitzland_auswahl",
    CAST("grössenklasse_gruppe" AS VARCHAR) AS "grössenklasse_gruppe",
    CAST("regionalisierungsgrad_der_gruppe" AS VARCHAR) AS "regionalisierungsgrad_der_gruppe",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0606010000-101"
