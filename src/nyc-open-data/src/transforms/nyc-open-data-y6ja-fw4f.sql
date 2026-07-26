-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "park_name",
    "feat_code",
    "source_id",
    "sub_code",
    "landuse",
    "parknum",
    "status",
    "_system" AS system,
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-y6ja-fw4f"
