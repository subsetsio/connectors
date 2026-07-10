-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table records annual status classifications by bathing water and zone type; quality, management, and monitoring-calendar columns are categorical statuses, not numeric measures.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "countryCode" AS countrycode,
    "management",
    "monitoringCalendar" AS monitoringcalendar,
    "quality",
    "qualityOriginalClassification" AS qualityoriginalclassification,
    "reportedSpecialisedZoneType" AS reportedspecialisedzonetype,
    "season",
    "specialisedZoneType" AS specialisedzonetype,
    "uid"
FROM "eea-bathing-water-assessment-bathingwaterstatus"
