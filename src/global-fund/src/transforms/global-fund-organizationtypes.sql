-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "parentId" AS parentid,
    "group",
    "name",
    "code",
    CAST("dateTimeCreated" AS TIMESTAMP) AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated
FROM "global-fund-organizationtypes"
