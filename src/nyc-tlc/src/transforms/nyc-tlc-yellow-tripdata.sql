-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are reported yellow taxi trip events without a stable trip identifier; repeated pickup and dropoff details can occur for distinct trips.
SELECT
    "VendorID" AS vendorid,
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID" AS ratecodeid,
    "store_and_fwd_flag",
    "PULocationID" AS pulocationid,
    "DOLocationID" AS dolocationid,
    CAST("payment_type" AS BIGINT) AS payment_type,
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
    "cbd_congestion_fee"
FROM "nyc-tlc-yellow-tripdata"
