-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("leistungsart" AS VARCHAR) AS "leistungsart",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("geburtsjahr_kind" AS VARCHAR) AS "geburtsjahr_kind",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304070000-102"
