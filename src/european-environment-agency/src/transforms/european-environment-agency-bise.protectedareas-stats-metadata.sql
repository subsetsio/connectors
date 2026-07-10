SELECT
    CAST("Dataset_title" AS VARCHAR) AS "Dataset_title",
    CAST("Link_SDI_or_external" AS VARCHAR) AS "Link_SDI_or_external",
    CAST("Version_date" AS VARCHAR) AS "Version_date"
FROM "european-environment-agency-bise.protectedareas-stats-metadata"
