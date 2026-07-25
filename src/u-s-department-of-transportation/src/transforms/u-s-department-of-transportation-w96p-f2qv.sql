-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "level",
    CAST("date" AS TIMESTAMP) AS date,
    "state_fips",
    "state_code",
    "county_fips",
    "county",
    CAST("pop_stay_at_home" AS DOUBLE) AS pop_stay_at_home,
    CAST("pop_not_stay_at_home" AS DOUBLE) AS pop_not_stay_at_home,
    CAST("trips" AS DOUBLE) AS trips,
    CAST("trips_1" AS DOUBLE) AS trips_1,
    CAST("trips_1_3" AS DOUBLE) AS trips_1_3,
    CAST("trips_3_5" AS DOUBLE) AS trips_3_5,
    CAST("trips_5_10" AS DOUBLE) AS trips_5_10,
    CAST("trips_10_25" AS DOUBLE) AS trips_10_25,
    CAST("trips_25_50" AS DOUBLE) AS trips_25_50,
    CAST("trips_50_100" AS DOUBLE) AS trips_50_100,
    CAST("trips_100_250" AS DOUBLE) AS trips_100_250,
    CAST("trips_250_500" AS DOUBLE) AS trips_250_500,
    CAST("trips_500" AS DOUBLE) AS trips_500,
    "row_id",
    CAST("week" AS BIGINT) AS week,
    CAST("month" AS BIGINT) AS month
FROM "u-s-department-of-transportation-w96p-f2qv"
