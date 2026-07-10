-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("grossregion" AS VARCHAR) AS "grossregion",
    CAST("tätigkeit" AS VARCHAR) AS "tätigkeit",
    CAST("anforderungsniveau_des_arbeitsplatzes" AS VARCHAR) AS "anforderungsniveau_des_arbeitsplatzes",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0304010000-101"
