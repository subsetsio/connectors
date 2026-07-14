-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "SEASONALITY" AS seasonality,
    "EQUIP" AS equip,
    "TOUR_MEASURE" AS tour_measure,
    "HOTEL_STA" AS hotel_sta,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "ACTIVITY" AS activity,
    "TOUR_RESID" AS tour_resid,
    "UNIT_LOC_RANKING" AS unit_loc_ranking,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-tour-freq"
