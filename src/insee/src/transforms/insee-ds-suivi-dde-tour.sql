-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "TOUR_MEASURE" AS tour_measure,
    "TRAVEL_DEST" AS travel_dest,
    "MODE_TRANSPORT" AS mode_transport,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "TYPE_TOUR_ACCOMODATION" AS type_tour_accomodation,
    "TRAVEL_REASON" AS travel_reason,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-suivi-dde-tour"
