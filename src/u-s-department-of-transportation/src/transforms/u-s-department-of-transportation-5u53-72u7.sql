-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("link_id" AS BIGINT) AS link_id,
    "name",
    CAST("osm_way_id" AS BIGINT) AS osm_way_id,
    CAST("from_node_id" AS BIGINT) AS from_node_id,
    CAST("to_node_id" AS BIGINT) AS to_node_id,
    CAST("directed" AS BIGINT) AS directed,
    "geometry",
    CAST("dir_flag" AS BIGINT) AS dir_flag,
    CAST("length" AS DOUBLE) AS length,
    "facility_type",
    CAST("link_type" AS BIGINT) AS link_type,
    CAST("free_speed" AS BIGINT) AS free_speed,
    "free_speed_raw",
    CAST("lanes" AS BIGINT) AS lanes,
    CAST("capacity" AS BIGINT) AS capacity,
    "allowed_uses",
    "toll",
    "notes"
FROM "u-s-department-of-transportation-5u53-72u7"
