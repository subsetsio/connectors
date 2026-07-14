-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "FACILITY_SDOM" AS facility_sdom,
    "BOARDING_SCHOOL" AS boarding_school,
    "RPI_TYPE" AS rpi_type,
    "EP" AS ep,
    "FACILITY_DOM" AS facility_dom,
    "GEO" AS geo,
    "BPE_MEASURE" AS bpe_measure,
    "CANTEEN" AS canteen,
    "CPGE" AS cpge,
    "FACILITY_TYPE" AS facility_type,
    "SCHOOL_SECTOR" AS school_sector,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-bpe-education"
