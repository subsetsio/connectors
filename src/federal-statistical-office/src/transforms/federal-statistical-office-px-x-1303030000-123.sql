-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("verwaltungsform" AS VARCHAR) AS "verwaltungsform",
    CAST("art_der_risikodeckung" AS VARCHAR) AS "art_der_risikodeckung",
    CAST("rechtsform" AS VARCHAR) AS "rechtsform",
    CAST("registrierung_ve" AS VARCHAR) AS "registrierung_ve",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1303030000-123"
