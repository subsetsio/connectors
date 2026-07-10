SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("location" AS VARCHAR) AS "location",
    CAST("pressurecode" AS VARCHAR) AS "pressurecode",
    CAST("ranking" AS VARCHAR) AS "ranking",
    CAST("report_obligation" AS VARCHAR) AS "report_obligation",
    CAST("season" AS VARCHAR) AS "season",
    CAST("speciescode" AS VARCHAR) AS "speciescode",
    CAST("speciesname" AS VARCHAR) AS "speciesname",
    CAST("sub_unit" AS VARCHAR) AS "sub_unit",
    CAST("type" AS VARCHAR) AS "type",
    CAST("use_for_statistics" AS VARCHAR) AS "use_for_statistics"
FROM "european-environment-agency-fise.n2k-art12-mastertab-data-bpressures-threats-published"
