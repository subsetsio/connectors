-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are daily movement distribution categories by geography; categories are parts of a distribution and should not be mixed without filtering.
SELECT
    "gadm_id",
    "gadm_name",
    "country",
    "polygon_level",
    "home_to_ping_distance_category",
    "distance_category_ping_fraction",
    "ds",
    "_source_file" AS source_file
FROM "meta-movement-distribution"
