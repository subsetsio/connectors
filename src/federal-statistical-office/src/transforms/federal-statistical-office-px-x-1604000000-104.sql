-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("e_commerce_und_e_banking" AS VARCHAR) AS "e_commerce_und_e_banking",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("bildungsstand" AS VARCHAR) AS "bildungsstand",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("absolut_relativ" AS VARCHAR) AS "absolut_relativ",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1604000000-104"
