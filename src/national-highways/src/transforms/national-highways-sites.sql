-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The register includes both active and inactive monitoring sites; filter status when current live coverage is required.
SELECT
    CAST("site_id" AS BIGINT) AS site_id,
    "name",
    "description",
    "longitude",
    "latitude",
    "status"
FROM "national-highways-sites"
