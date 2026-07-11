-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "surveyName" AS surveyname,
    "surveyShortName" AS surveyshortname,
    "survey",
    "surveyDescription" AS surveydescription,
    "surveyUrl" AS surveyurl,
    "questionnaireUrl" AS questionnaireurl,
    "publicUseUrl" AS publicuseurl,
    "surveyType" AS surveytype,
    "surveyYearsCollected" AS surveyyearscollected,
    "surveyFrequency" AS surveyfrequency,
    "responseUnit" AS responseunit,
    "surveyPopulation" AS surveypopulation,
    "topics",
    "surveyGroupName" AS surveygroupname
FROM "ncses-surveys"
