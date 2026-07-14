-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "TYPE_INDICATOR_SDG" AS type_indicator_sdg,
    "PCS" AS pcs,
    "BASE_PER" AS base_per,
    "SDG" AS sdg,
    "SEX" AS sex,
    "EMPSTA" AS empsta,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "INDICATOR_SDG" AS indicator_sdg,
    "UNIT_MEASURE" AS unit_measure,
    "COMPOSITE_BREAKDOWN" AS composite_breakdown,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-nat-sdg"
