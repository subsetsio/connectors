-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Site rows are scoped to study records, so the same NOAA site can appear in more than one study.
SELECT
    "study_id",
    "site_id",
    "site_name",
    "site_code",
    "mappable",
    "location_name",
    "geo_type",
    "geometry_type",
    "geometry_coordinates_json",
    "southernmost_latitude",
    "northernmost_latitude",
    "westernmost_longitude",
    "easternmost_longitude",
    "min_elevation_meters",
    "max_elevation_meters",
    "study_contribution_date"
FROM "itrdb-sites"
