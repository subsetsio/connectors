-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("internetzugang" AS VARCHAR) AS "internetzugang",
    CAST("sprachgebiet" AS VARCHAR) AS "sprachgebiet",
    CAST("haushaltsgrösse" AS VARCHAR) AS "haushaltsgrösse",
    CAST("subjektive_finanzielle_situation_des_haushalts" AS VARCHAR) AS "subjektive_finanzielle_situation_des_haushalts",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("absolut_relativ" AS VARCHAR) AS "absolut_relativ",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1604000000-101"
