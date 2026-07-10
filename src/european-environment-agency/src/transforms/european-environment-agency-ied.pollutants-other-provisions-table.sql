SELECT
    CAST("id" AS VARCHAR) AS "id",
    CAST("other_provision_id" AS VARCHAR) AS "other_provision_id",
    CAST("other_provision_sub" AS VARCHAR) AS "other_provision_sub",
    CAST("other_provision_text" AS VARCHAR) AS "other_provision_text",
    CAST("other_provision_type" AS VARCHAR) AS "other_provision_type"
FROM "european-environment-agency-ied.pollutants-other-provisions-table"
