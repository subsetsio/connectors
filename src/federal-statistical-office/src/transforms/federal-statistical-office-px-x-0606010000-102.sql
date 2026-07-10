-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("wirtschaftliche_tätigkeit_bfs50" AS VARCHAR) AS "wirtschaftliche_tätigkeit_bfs50",
    CAST("grössenklasse_gruppe" AS VARCHAR) AS "grössenklasse_gruppe",
    CAST("art_der_gruppe" AS VARCHAR) AS "art_der_gruppe",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0606010000-102"
