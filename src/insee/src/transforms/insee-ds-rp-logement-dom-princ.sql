-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census tables can include geographic aggregates and categorical totals together with detailed categories; filter geography and category dimensions before summing observations.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "GEO" AS geo,
    "WW" AS ww,
    "AIRCOND" AS aircond,
    "ELEC" AS elec,
    "BAINWC" AS bainwc,
    "TDW" AS tdw,
    "WSS" AS wss,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "RP_MEASURE" AS rp_measure,
    "OCS" AS ocs,
    "SOBO" AS sobo,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-rp-logement-dom-princ"
