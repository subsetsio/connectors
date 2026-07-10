-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kosten_und_erlöse" AS VARCHAR) AS "kosten_und_erlöse",
    CAST("betriebstyp" AS VARCHAR) AS "betriebstyp",
    CAST("leistungstyp" AS VARCHAR) AS "leistungstyp",
    CAST("aktivität" AS VARCHAR) AS "aktivität",
    CAST("garant" AS VARCHAR) AS "garant",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404010100-105"
