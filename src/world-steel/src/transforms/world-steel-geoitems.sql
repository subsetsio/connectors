-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes both countries and regional aggregate geographies; filter or group by the geography metadata before summing observations joined from the values table.
SELECT
    "geoitem_id",
    "type",
    "label",
    CAST("wsa" AS BIGINT) AS wsa,
    CAST("order_id" AS BIGINT) AS order_id,
    "color",
    "regions_json",
    "children_json",
    "metadata_json"
FROM "world-steel-geoitems"
