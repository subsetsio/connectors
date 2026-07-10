-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("online_dienste_in_zusammenhang_mit_den_behörden" AS VARCHAR) AS "online_dienste_in_zusammenhang_mit_den_behörden",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("bildungsstand" AS VARCHAR) AS "bildungsstand",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("absolut_relativ" AS VARCHAR) AS "absolut_relativ",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1604000000-103"
