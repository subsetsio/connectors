-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are daily movement range metrics by polygon; compare values within the same polygon_level and polygon_version context.
SELECT
    "ds",
    "country",
    "polygon_source",
    "polygon_id",
    "polygon_name",
    "all_day_bing_tiles_visited_relative_change",
    "all_day_ratio_single_tile_users",
    "baseline_name",
    "baseline_type",
    "_source_file" AS source_file
FROM "meta-movement-range-maps"
