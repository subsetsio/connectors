-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton_gemeinde" AS VARCHAR) AS "kanton_gemeinde",
    CAST("kategorie_der_auftraggeber" AS VARCHAR) AS "kategorie_der_auftraggeber",
    CAST("art_der_bauwerke" AS VARCHAR) AS "art_der_bauwerke",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0904010000-112"
