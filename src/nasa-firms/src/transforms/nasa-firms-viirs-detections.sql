-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are individual VIIRS active-fire detections rather than area or incident summaries; multiple detections can refer to the same fire event across times, pixels, and satellites.
-- caution: Historical SNPP archive rows carry a derived country from FIRMS country files, while the rolling recent global feeds for SNPP, NOAA-20, and NOAA-21 can have no country value.
SELECT
    "country",
    "latitude",
    "longitude",
    "bright_ti4",
    "scan",
    "track",
    "bright_ti5",
    "frp",
    strptime("acq_date", '%Y-%m-%d')::DATE AS acq_date,
    "acq_time",
    "satellite",
    "instrument",
    "confidence",
    "version",
    "daynight",
    CAST("type" AS BIGINT) AS type
FROM "nasa-firms-viirs-detections"
