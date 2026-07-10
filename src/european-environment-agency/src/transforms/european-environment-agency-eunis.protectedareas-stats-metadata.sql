SELECT
    CAST("Dataset_title" AS VARCHAR) AS "Dataset_title",
    CAST("Link_SDI_or_external" AS VARCHAR) AS "Link_SDI_or_external",
    CAST("Source_dataset" AS VARCHAR) AS "Source_dataset",
    CAST("Version_date" AS VARCHAR) AS "Version_date"
FROM "european-environment-agency-eunis.protectedareas-stats-metadata"
