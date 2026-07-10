SELECT
    CAST("comment" AS VARCHAR) AS "comment",
    CAST("dataset" AS VARCHAR) AS "dataset",
    CAST("update_date" AS VARCHAR) AS "update_date",
    CAST("version_details" AS VARCHAR) AS "version_details"
FROM "european-environment-agency-eunis.a2-dataset-update-details"
