-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Date precision varies by eruption: year, month, day, and uncertainty fields are separate source columns, so filter on the precision fields before doing day- or month-level time analysis.
SELECT
    "FID" AS fid,
    CAST("Volcano_Number" AS BIGINT) AS volcano_number,
    "Volcano_Name" AS volcano_name,
    CAST("Eruption_Number" AS BIGINT) AS eruption_number,
    "Activity_Type" AS activity_type,
    CAST("ExplosivityIndexMax" AS BIGINT) AS explosivityindexmax,
    "ExplosivityIndexModifier" AS explosivityindexmodifier,
    "ActivityArea" AS activityarea,
    "ActivityUnit" AS activityunit,
    "StartEvidenceMethod" AS startevidencemethod,
    "StartDateYearModifier" AS startdateyearmodifier,
    CAST("StartDateYear" AS BIGINT) AS startdateyear,
    CAST("StartDateYearUncertainty" AS BIGINT) AS startdateyearuncertainty,
    "StartDateDayModifier" AS startdatedaymodifier,
    CAST("StartDateMonth" AS BIGINT) AS startdatemonth,
    CAST("StartDateDay" AS BIGINT) AS startdateday,
    CAST("StartDateDayUncertainty" AS BIGINT) AS startdatedayuncertainty,
    "EndDateYearModifier" AS enddateyearmodifier,
    CAST("EndDateYear" AS BIGINT) AS enddateyear,
    CAST("EndDateYearUncertainty" AS BIGINT) AS enddateyearuncertainty,
    "EndDateDayModifier" AS enddatedaymodifier,
    CAST("EndDateMonth" AS BIGINT) AS enddatemonth,
    CAST("EndDateDay" AS BIGINT) AS enddateday,
    CAST("EndDateDayUncertainty" AS BIGINT) AS enddatedayuncertainty,
    "GeoLocation" AS geolocation
FROM "global-volcanism-program-smithsonian-votw-holocene-eruptions"
