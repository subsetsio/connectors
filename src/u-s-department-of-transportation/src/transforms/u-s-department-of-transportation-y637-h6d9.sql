-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("features_properties__id" AS BIGINT) AS features_properties_id,
    CAST("features_properties_ext_osm_version" AS BIGINT) AS features_properties_ext_osm_version,
    "features_properties_highway",
    "features_properties_footway",
    "features_properties_surface",
    "features_properties_crossing_markings",
    CAST("features_properties_length" AS DOUBLE) AS features_properties_length,
    CAST("features_properties_incline" AS DOUBLE) AS features_properties_incline,
    CAST("features_properties__u_id" AS BIGINT) AS features_properties_u_id,
    CAST("features_properties__v_id" AS BIGINT) AS features_properties_v_id
FROM "u-s-department-of-transportation-y637-h6d9"
