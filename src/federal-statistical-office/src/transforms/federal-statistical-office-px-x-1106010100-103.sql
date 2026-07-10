-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unfallschwere" AS VARCHAR) AS "unfallschwere",
    CAST("strassenart" AS VARCHAR) AS "strassenart",
    CAST("unfallort" AS VARCHAR) AS "unfallort",
    CAST("erlaubte_höchstgeschwindigkeit" AS VARCHAR) AS "erlaubte_höchstgeschwindigkeit",
    CAST("relevante_vortrittsregelung" AS VARCHAR) AS "relevante_vortrittsregelung",
    CAST("strassenzustand" AS VARCHAR) AS "strassenzustand",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1106010100-103"
