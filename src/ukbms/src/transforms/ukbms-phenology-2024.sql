-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source contains duplicate site/species/year phenology records, including exact duplicate rows, so consumers should deduplicate or aggregate deliberately before site-year analysis.
-- caution: FIRSTDAY, LASTDAY, PEAKDAY, and related flight-period fields are day offsets in the source, not calendar dates.
SELECT
    "SITENO" AS siteno,
    "SITENAME" AS sitename,
    "GRIDREF" AS gridref,
    "SPECIES_NAME" AS species_name,
    "COMMON_NAME" AS common_name,
    "YEAR" AS year,
    "FIRSTDAY" AS firstday,
    "LASTDAY" AS lastday,
    "PEAKDAY" AS peakday,
    "PEAKCOUNT" AS peakcount,
    "MEAN_FLIGHT_DATE" AS mean_flight_date,
    "FLIGHTPERIOD_SD" AS flightperiod_sd,
    "FLIGHTPERIOD_RANGE" AS flightperiod_range
FROM "ukbms-phenology-2024"
