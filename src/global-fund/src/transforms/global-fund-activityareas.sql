-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "type",
    "name",
    "code",
    "iatI_Code" AS iati_code,
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated,
    "parentId" AS parentid
FROM "global-fund-activityareas"
