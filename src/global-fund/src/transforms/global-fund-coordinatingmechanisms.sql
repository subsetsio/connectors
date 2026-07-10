-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes exact duplicate coordinating mechanism rows and duplicated ids; deduplicate by the full row or by the intended geography/name fields before counting mechanisms.
SELECT
    "id",
    "name",
    "website",
    "geographyId" AS geographyid,
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated
FROM "global-fund-coordinatingmechanisms"
