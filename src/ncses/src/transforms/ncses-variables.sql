-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "universalId" AS universalid,
    CAST("variableId" AS BIGINT) AS variableid,
    "variableType" AS variabletype,
    "variableName" AS variablename,
    "title",
    "variableShortName" AS variableshortname,
    "qlikName" AS qlikname,
    "variableShortDescription" AS variableshortdescription,
    "measures",
    "units",
    "variableYearsAvailable" AS variableyearsavailable,
    "showInBuilder" AS showinbuilder,
    "surveyShortName" AS surveyshortname,
    "survey",
    "topics",
    "measureGroupName" AS measuregroupname
FROM "ncses-variables"
