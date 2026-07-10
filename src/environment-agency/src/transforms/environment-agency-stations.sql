-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Station reference rows describe monitoring locations and should be joined to measures or readings before interpreting observed values.
SELECT
    "station_guid",
    "name",
    "notation",
    "wiski_id",
    "river_name",
    "easting",
    "northing",
    "lat",
    "long",
    strptime("date_opened", '%Y-%m-%d')::DATE AS date_opened,
    "status",
    "observed_properties",
    "n_measures"
FROM "environment-agency-stations"
