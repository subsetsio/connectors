-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("berufliche_tätigkeit" AS VARCHAR) AS "berufliche_tätigkeit",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-4003000000-163"
