-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Station records include both active and inactive monitoring sites; use the active date columns when analyzing availability for a specific period.
SELECT
    "station_id",
    "station_code",
    "station_name",
    "station_city",
    "station_synonym",
    "station_active_from",
    "station_active_to",
    "station_longitude",
    "station_latitude",
    "network_id",
    "station_setting_id",
    "station_type_id",
    "network_code",
    "network_name",
    "station_setting_name",
    "station_setting_short_name",
    "station_type_name",
    "station_street",
    "station_street_nr",
    "station_zip_code"
FROM "umweltbundesamt-stations"
