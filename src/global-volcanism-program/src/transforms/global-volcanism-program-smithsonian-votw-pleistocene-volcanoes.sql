-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table covers Pleistocene volcanoes and is not a historical continuation of the Holocene volcano table; analyze it as a separate reference population.
SELECT
    "FID" AS fid,
    CAST("Volcano_Number" AS BIGINT) AS volcano_number,
    "Volcano_Name" AS volcano_name,
    "Volcanic_Landform" AS volcanic_landform,
    "Primary_Volcano_Type" AS primary_volcano_type,
    "Country" AS country,
    "Region" AS region,
    "Subregion" AS subregion,
    "Geological_Summary" AS geological_summary,
    CAST("Latitude" AS DOUBLE) AS latitude,
    CAST("Longitude" AS DOUBLE) AS longitude,
    CAST("Elevation" AS BIGINT) AS elevation,
    "Geologic_Epoch" AS geologic_epoch,
    "GeoLocation" AS geolocation
FROM "global-volcanism-program-smithsonian-votw-pleistocene-volcanoes"
