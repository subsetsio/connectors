SELECT
    CAST("description" AS VARCHAR) AS "description",
    CAST("pollutant_group_id" AS VARCHAR) AS "pollutant_group_id",
    CAST("sub" AS VARCHAR) AS "sub"
FROM "european-environment-agency-ied.pollutants-groups-details-table"
