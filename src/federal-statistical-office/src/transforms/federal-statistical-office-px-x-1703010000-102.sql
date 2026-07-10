-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("periode" AS VARCHAR) AS "periode",
    CAST("abstimmungsvorlage_typ" AS VARCHAR) AS "abstimmungsvorlage_typ",
    CAST("abstimmungsvorlage_angenommen_verworfen" AS VARCHAR) AS "abstimmungsvorlage_angenommen_verworfen",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1703010000-102"
