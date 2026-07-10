-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This E3 web-app layer is a recent-era eruption view and overlaps the broader Holocene eruptions catalog; do not combine the two eruption tables without deduplicating by source identifiers and date fields.
SELECT
    "FID" AS fid,
    CAST("VolcanoNumber" AS BIGINT) AS volcanonumber,
    "VolcanoName" AS volcanoname,
    CAST("ExplosivityIndexMax" AS BIGINT) AS explosivityindexmax,
    strptime("StartDate", '%Y%m%d')::DATE AS startdate,
    CAST("StartDateYear" AS BIGINT) AS startdateyear,
    CAST("StartDateMonth" AS BIGINT) AS startdatemonth,
    CAST("StartDateDay" AS BIGINT) AS startdateday,
    strptime("EndDate", '%Y%m%d')::DATE AS enddate,
    CAST("EndDateYear" AS BIGINT) AS enddateyear,
    CAST("EndDateMonth" AS BIGINT) AS enddatemonth,
    CAST("EndDateDay" AS BIGINT) AS enddateday,
    CAST("ContinuingEruption" AS BOOLEAN) AS continuingeruption,
    CAST("LatitudeDecimal" AS DOUBLE) AS latitudedecimal,
    CAST("LongitudeDecimal" AS DOUBLE) AS longitudedecimal,
    "GeoLocation" AS geolocation,
    CAST("Activity_ID" AS BIGINT) AS activity_id
FROM "global-volcanism-program-e3webapp-eruptions1960"
