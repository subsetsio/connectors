-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the canonical Holocene volcano reference; `Last_Eruption_Year` is a source attribute about the volcano record, not a row observation period.
SELECT
    "FID" AS fid,
    CAST("Volcano_Number" AS BIGINT) AS volcano_number,
    "Volcano_Name" AS volcano_name,
    "Volcanic_Landform" AS volcanic_landform,
    "Primary_Volcano_Type" AS primary_volcano_type,
    CAST("Last_Eruption_Year" AS BIGINT) AS last_eruption_year,
    "Country" AS country,
    "Region" AS region,
    "Subregion" AS subregion,
    "Geological_Summary" AS geological_summary,
    CAST("Latitude" AS DOUBLE) AS latitude,
    CAST("Longitude" AS DOUBLE) AS longitude,
    CAST("Elevation" AS BIGINT) AS elevation,
    "Tectonic_Setting" AS tectonic_setting,
    "Geologic_Epoch" AS geologic_epoch,
    "Evidence_Category" AS evidence_category,
    "Primary_Photo_Link" AS primary_photo_link,
    "Primary_Photo_Caption" AS primary_photo_caption,
    "Primary_Photo_Credit" AS primary_photo_credit,
    "Major_Rock_Type" AS major_rock_type,
    "GeoLocation" AS geolocation
FROM "global-volcanism-program-smithsonian-votw-holocene-volcanoes"
