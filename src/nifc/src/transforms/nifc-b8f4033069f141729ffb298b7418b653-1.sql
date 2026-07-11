-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "BRIGHTNESS" AS brightness,
    "SCAN" AS scan,
    "TRACK" AS track,
    "SATELLITE" AS satellite,
    "CONFIDENCE" AS confidence,
    "VERSION" AS version,
    "BRIGHT_T31" AS bright_t31,
    "FRP" AS frp,
    "ACQ_DATE" AS acq_date,
    "DAYNIGHT" AS daynight,
    "HOURS_OLD" AS hours_old,
    "DAY_OF_ACQ" AS day_of_acq
FROM "nifc-b8f4033069f141729ffb298b7418b653-1"
