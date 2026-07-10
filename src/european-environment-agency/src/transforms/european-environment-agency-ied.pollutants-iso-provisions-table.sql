SELECT
    CAST("id" AS VARCHAR) AS "id",
    CAST("pollutantId" AS VARCHAR) AS "pollutantId",
    CAST("standard" AS VARCHAR) AS "standard",
    CAST("target" AS VARCHAR) AS "target",
    CAST("title" AS VARCHAR) AS "title",
    CAST("uncertainty_sup" AS VARCHAR) AS "uncertainty_sup",
    CAST("uncertainty_text" AS VARCHAR) AS "uncertainty_text"
FROM "european-environment-agency-ied.pollutants-iso-provisions-table"
