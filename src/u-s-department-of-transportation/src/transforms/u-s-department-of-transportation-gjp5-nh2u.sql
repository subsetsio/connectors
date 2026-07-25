-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "rpcarrier",
    CAST("average_market_fare_real" AS BIGINT) AS average_market_fare_real,
    CAST("market_passengers" AS BIGINT) AS market_passengers,
    CAST("market_revenue_real" AS BIGINT) AS market_revenue_real,
    CAST("market_passenger_miles_flown" AS BIGINT) AS market_passenger_miles_flown,
    CAST("average_market_yield_real" AS DOUBLE) AS average_market_yield_real,
    CAST("average_market_miles_flown" AS DOUBLE) AS average_market_miles_flown,
    "carrier_name"
FROM "u-s-department-of-transportation-gjp5-nh2u"
