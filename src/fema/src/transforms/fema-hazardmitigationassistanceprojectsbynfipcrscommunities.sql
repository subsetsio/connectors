-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "projectIdentifier" AS projectidentifier,
    "communityName" AS communityname,
    "communityNumber" AS communitynumber,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-hazardmitigationassistanceprojectsbynfipcrscommunities"
