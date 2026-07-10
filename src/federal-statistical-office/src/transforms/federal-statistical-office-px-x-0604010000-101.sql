-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("struktur_der_bilanz_der_unternehmen" AS VARCHAR) AS "struktur_der_bilanz_der_unternehmen",
    CAST("wirtschaftsabteilung" AS VARCHAR) AS "wirtschaftsabteilung",
    CAST("grössenklasse" AS VARCHAR) AS "grössenklasse",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0604010000-101"
