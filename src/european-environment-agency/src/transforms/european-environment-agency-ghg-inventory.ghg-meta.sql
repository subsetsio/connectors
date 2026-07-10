SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_code_3" AS VARCHAR) AS "country_code_3",
    CAST("submission_version" AS VARCHAR) AS "submission_version",
    CAST("submission_year" AS VARCHAR) AS "submission_year"
FROM "european-environment-agency-ghg-inventory.ghg-meta"
