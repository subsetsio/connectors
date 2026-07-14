-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census tables can include geographic aggregates and categorical totals together with detailed categories; filter geography and category dimensions before summing observations.
SELECT
    "CARS" AS cars,
    "BUILD_END" AS build_end,
    "NRG_SRC" AS nrg_src,
    "TDW" AS tdw,
    "TSH" AS tsh,
    "CARPARK" AS carpark,
    "RP_MEASURE" AS rp_measure,
    "GEO" AS geo,
    "NOR" AS nor,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OCS" AS ocs,
    "L_STAY" AS l_stay,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-rp-logement-princ"
