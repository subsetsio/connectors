SELECT
    CAST("code" AS VARCHAR) AS "code",
    CAST("coordinatingInstitution" AS VARCHAR) AS "coordinatingInstitution",
    CAST("created" AS VARCHAR) AS "created",
    CAST("end" AS VARCHAR) AS "end",
    CAST("endDate" AS VARCHAR) AS "endDate",
    CAST("id" AS VARCHAR) AS "id",
    CAST("logo" AS VARCHAR) AS "logo",
    CAST("logoFilename" AS VARCHAR) AS "logoFilename",
    CAST("objectives" AS VARCHAR) AS "objectives",
    CAST("participatingCountries" AS VARCHAR) AS "participatingCountries",
    CAST("projectName" AS VARCHAR) AS "projectName",
    CAST("projectNameShort" AS VARCHAR) AS "projectNameShort",
    CAST("start" AS VARCHAR) AS "start",
    CAST("startDate" AS VARCHAR) AS "startDate",
    CAST("updated" AS VARCHAR) AS "updated",
    CAST("url" AS VARCHAR) AS "url"
FROM "european-environment-agency-fise.v-fise-research-project-catalogue"
