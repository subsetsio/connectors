SELECT
    CAST("code" AS VARCHAR) AS "code",
    CAST("coordinatingInstitution" AS VARCHAR) AS "coordinatingInstitution",
    CAST("created" AS VARCHAR) AS "created",
    CAST("endDate" AS VARCHAR) AS "endDate",
    CAST("logo" AS VARCHAR) AS "logo",
    CAST("logoFilename" AS VARCHAR) AS "logoFilename",
    CAST("objectives" AS VARCHAR) AS "objectives",
    CAST("participatingCountries" AS VARCHAR) AS "participatingCountries",
    CAST("projectName" AS VARCHAR) AS "projectName",
    CAST("startDate" AS VARCHAR) AS "startDate",
    CAST("updated" AS VARCHAR) AS "updated",
    CAST("url" AS VARCHAR) AS "url"
FROM "european-environment-agency-fise.research-project"
