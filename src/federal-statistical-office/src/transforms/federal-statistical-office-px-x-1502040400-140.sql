-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("wohnkanton_vor_studienbeginn" AS VARCHAR) AS "wohnkanton_vor_studienbeginn",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502040400-140"
