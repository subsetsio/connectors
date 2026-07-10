-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a board-constituency geography hierarchy view, not a pure country list; filter level before using it as a country dimension.
SELECT
    "id",
    "code",
    "isO2" AS iso2,
    "level",
    "name",
    "legalName" AS legalname,
    CAST("dateTimeCreated" AS TIMESTAMP) AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated,
    "parentId" AS parentid,
    "isDonor" AS isdonor,
    "isRecipient" AS isrecipient
FROM "global-fund-geographies-boardconstituencyview"
