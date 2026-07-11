-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Quarter" AS quarter,
    "QuarterQF" AS quarterqf,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "Location" AS location,
    "LocationQF" AS locationqf,
    "Specialty" AS specialty,
    "SpecialtyQF" AS specialtyqf,
    "SpecialtyName" AS specialtyname,
    "SpecialtyNameQF" AS specialtynameqf,
    CAST("AllStaffedBeddays" AS BIGINT) AS allstaffedbeddays,
    "AllStaffedBeddaysQF" AS allstaffedbeddaysqf,
    CAST("TotalOccupiedBeddays" AS BIGINT) AS totaloccupiedbeddays,
    "TotalOccupiedBeddaysQF" AS totaloccupiedbeddaysqf,
    CAST("AverageAvailableStaffedBeds" AS DOUBLE) AS averageavailablestaffedbeds,
    "AverageAvailableStaffedBedsQF" AS averageavailablestaffedbedsqf,
    CAST("AverageOccupiedBeds" AS DOUBLE) AS averageoccupiedbeds,
    "AverageOccupiedBedsQF" AS averageoccupiedbedsqf,
    CAST("PercentageOccupancy" AS DOUBLE) AS percentageoccupancy,
    "PercentageOccupancyQF" AS percentageoccupancyqf,
    "loc_name",
    "dqNotesIP" AS dqnotesip,
    "dqNotesOP" AS dqnotesop,
    "dqNotesBeds" AS dqnotesbeds
FROM "public-health-scotland-hospital-beds-information"
