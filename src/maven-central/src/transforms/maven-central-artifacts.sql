-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe artifact coordinates and the latest version observed in the repository index, not every historical artifact version.
SELECT
    "group_id",
    "artifact_id",
    "latest_version",
    "packaging",
    "version_count",
    "repository_id",
    "last_updated"
FROM "maven-central-artifacts"
