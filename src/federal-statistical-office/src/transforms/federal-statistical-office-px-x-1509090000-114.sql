-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("szenario" AS VARCHAR) AS "szenario",
    CAST("hochschultyp" AS VARCHAR) AS "hochschultyp",
    CAST("niveau" AS VARCHAR) AS "niveau",
    CAST("zulassungsausweis" AS VARCHAR) AS "zulassungsausweis",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1509090000-114"
