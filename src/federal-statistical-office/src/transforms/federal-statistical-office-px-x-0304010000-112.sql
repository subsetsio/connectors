-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("grossregion" AS VARCHAR) AS "grossregion",
    CAST("staatsangehörigkeit_anwesenheitsbewilligung" AS VARCHAR) AS "staatsangehörigkeit_anwesenheitsbewilligung",
    CAST("anforderungsniveau_des_arbeitsplatzes" AS VARCHAR) AS "anforderungsniveau_des_arbeitsplatzes",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("zentralwert_und_quartilbereich" AS VARCHAR) AS "zentralwert_und_quartilbereich",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0304010000-112"
