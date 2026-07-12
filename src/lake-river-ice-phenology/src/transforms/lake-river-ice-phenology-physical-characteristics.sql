-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a waterbody reference table, but `lakecode` alone is not unique in the measured raw data.
SELECT
    "lakecode",
    "lakename",
    "lakeorriver",
    "continent",
    "country",
    "state",
    "latitude",
    "longitude",
    CAST("elevation" AS DOUBLE) AS elevation,
    CAST("mean_depth" AS DOUBLE) AS mean_depth,
    CAST("max_depth" AS DOUBLE) AS max_depth,
    CAST("surface_area" AS DOUBLE) AS surface_area,
    CAST("shoreline" AS DOUBLE) AS shoreline,
    CAST("largest_city_population" AS BIGINT) AS largest_city_population,
    "power_plant_discharge",
    "inlet_streams",
    CAST("area_drained" AS BIGINT) AS area_drained,
    "landuse_code",
    CAST("conductivity_us" AS DOUBLE) AS conductivity_us,
    CAST("secchi_depth" AS DOUBLE) AS secchi_depth,
    "contributor",
    "filename",
    "initials",
    CAST("lat_decimal" AS DOUBLE) AS lat_decimal,
    CAST("lon_decimal" AS DOUBLE) AS lon_decimal,
    CAST("median_depth" AS DOUBLE) AS median_depth,
    "comments"
FROM "lake-river-ice-phenology-physical-characteristics"
