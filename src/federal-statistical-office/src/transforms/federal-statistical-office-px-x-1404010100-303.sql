-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("grossregion_kanton" AS VARCHAR) AS "grossregion_kanton",
    CAST("beherbergungstyp" AS VARCHAR) AS "beherbergungstyp",
    CAST("pflegeintensitätsstufe" AS VARCHAR) AS "pflegeintensitätsstufe",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404010100-303"
