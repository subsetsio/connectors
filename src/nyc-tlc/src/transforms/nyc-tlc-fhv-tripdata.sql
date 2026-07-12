-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are reported trip events without a stable trip identifier; do not treat any combination of timestamps, bases, and locations as a durable primary key.
SELECT
    "dispatching_base_num",
    "pickup_datetime",
    "dropoff_datetime",
    "PULocationID" AS pulocationid,
    "DOLocationID" AS dolocationid,
    "SR_Flag" AS sr_flag,
    "Affiliated_base_number" AS affiliated_base_number
FROM "nyc-tlc-fhv-tripdata"
