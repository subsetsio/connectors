-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    CAST("node_id" AS BIGINT) AS node_id,
    CAST("osm_node_id" AS BIGINT) AS osm_node_id,
    "ctrl_type",
    CAST("x_coord" AS DOUBLE) AS x_coord,
    CAST("y_coord" AS DOUBLE) AS y_coord,
    CAST("is_boundary" AS BIGINT) AS is_boundary,
    "activity_type",
    "poi_id",
    CAST("zone_id" AS BIGINT) AS zone_id,
    "notes"
FROM "u-s-department-of-transportation-rz4h-qbdn"
