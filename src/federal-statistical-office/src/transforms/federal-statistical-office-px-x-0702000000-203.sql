-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("familienmitglieder" AS VARCHAR) AS "familienmitglieder",
    CAST("leitung_betriebseigentum_erwerbstätigkeit_und_soziale_absicherung" AS VARCHAR) AS "leitung_betriebseigentum_erwerbstätigkeit_und_soziale_absicherung",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("einheit" AS VARCHAR) AS "einheit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-203"
