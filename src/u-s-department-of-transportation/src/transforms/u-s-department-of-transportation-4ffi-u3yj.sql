-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "features_geometry_coordinates",
    CAST("features_properties_ext_osm_version" AS BIGINT) AS features_properties_ext_osm_version,
    "features_properties_barrier",
    CAST("features_properties__id" AS BIGINT) AS features_properties_id
FROM "u-s-department-of-transportation-4ffi-u3yj"
