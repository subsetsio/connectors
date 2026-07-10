-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("geburtsjahrgang" AS VARCHAR) AS "geburtsjahrgang",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("alter" AS VARCHAR) AS "alter",
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020300-101"
