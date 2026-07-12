-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table unions multiple crisis-specific files with differing geographic fields and no stable non-null row identifier across all files.
-- caution: Rows are daily activity measures by crisis file, geography, and sometimes business vertical; do not sum activity_quantile.
SELECT
    "polygon_id",
    "polygon_name",
    "polygon_level",
    "polygon_version",
    "country",
    "business_vertical",
    "activity_quantile",
    "latitude",
    "longitude",
    "ds",
    "_source_file" AS source_file
FROM "meta-facebook-business-activity-trends-during-crisis"
