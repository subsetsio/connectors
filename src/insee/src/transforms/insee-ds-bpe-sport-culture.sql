-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "LIGHTED" AS lighted,
    "SANITARY" AS sanitary,
    "SANITARY_ACCESSIBILITY" AS sanitary_accessibility,
    "FACILITY_SDOM" AS facility_sdom,
    "SEASONAL_OPENING" AS seasonal_opening,
    "FREE_ACCESS" AS free_access,
    "MULTIPLEX_CINEMA" AS multiplex_cinema,
    "FACILITY_DOM" AS facility_dom,
    "INDOOR" AS indoor,
    "GEO" AS geo,
    "BPE_MEASURE" AS bpe_measure,
    "LOCKER_ROOM_ACCESSIBILITY" AS locker_room_accessibility,
    "SHOWER" AS shower,
    "FACILITY_TYPE" AS facility_type,
    "PRACTICE_AREA_ACCESSIBILITY" AS practice_area_accessibility,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "ERP_CATEGORY" AS erp_category,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-bpe-sport-culture"
