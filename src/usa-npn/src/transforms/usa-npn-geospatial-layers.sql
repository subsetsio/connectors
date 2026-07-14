-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Layer records describe GeoServer products, not station observations; dimension_values may encode available time steps or bands for a layer.
SELECT
    "name",
    "title",
    "abstract",
    "dimension_name",
    "dimension_values"
FROM "usa-npn-geospatial-layers"
