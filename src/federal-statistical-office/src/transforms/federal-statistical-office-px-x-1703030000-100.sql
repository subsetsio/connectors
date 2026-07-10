-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("datum_und_vorlage" AS VARCHAR) AS "datum_und_vorlage",
    CAST("ergebnis" AS VARCHAR) AS "ergebnis",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1703030000-100"
