-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "typeId" AS typeid,
    "geographyId" AS geographyid,
    "activityAreaId" AS activityareaid,
    "index",
    "title",
    "language",
    "url"
FROM "global-fund-documents"
