-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census tables can include geographic aggregates and categorical totals together with detailed categories; filter geography and category dimensions before summing observations.
SELECT
    "GEO" AS geo,
    "SEX" AS sex,
    "EMPFORM" AS empform,
    "FREQ" AS freq,
    CAST("EMPSTA_ENQ" AS BIGINT) AS empsta_enq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "WKTIME" AS wktime,
    "RP_MEASURE" AS rp_measure,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-rp-td-emploi-lt-empformwktime-comp"
