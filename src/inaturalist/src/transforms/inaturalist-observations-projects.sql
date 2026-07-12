-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a many-to-many membership table; joining it to observations can duplicate observation rows when an observation belongs to multiple projects.
-- caution: The natural row identifier is the observation_uuid/project_id pair, but the table is published as keyless because exact uniqueness verification over the large membership snapshot was not practical in the local model profiler.
SELECT
    "observation_uuid",
    CAST("project_id" AS BIGINT) AS "project_id"
FROM "inaturalist-observations-projects"
