-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("infrastruktur" AS VARCHAR) AS "infrastruktur",
    CAST("geräte_und_untersuchungen" AS VARCHAR) AS "geräte_und_untersuchungen",
    CAST("grossregion_kanton" AS VARCHAR) AS "grossregion_kanton",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404010100-101"
