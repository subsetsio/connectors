-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "segmentid",
    CAST("link_id" AS BIGINT) AS link_id,
    CAST("osm_way_id" AS BIGINT) AS osm_way_id
FROM "u-s-department-of-transportation-vtuk-ngz3"
