-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are reported green taxi trip events without a stable trip identifier; repeated pickup and dropoff details can occur for distinct trips.
SELECT
    "VendorID" AS vendorid,
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "store_and_fwd_flag",
    "RatecodeID" AS ratecodeid,
    "PULocationID" AS pulocationid,
    "DOLocationID" AS dolocationid,
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "ehail_fee",
    "improvement_surcharge",
    "total_amount",
    "payment_type",
    "trip_type",
    "congestion_surcharge",
    "cbd_congestion_fee"
FROM "nyc-tlc-green-tripdata"
