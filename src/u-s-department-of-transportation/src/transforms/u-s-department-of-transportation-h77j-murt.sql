-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("average_market_fare_real" AS BIGINT) AS average_market_fare_real,
    CAST("market_passengers" AS BIGINT) AS market_passengers,
    CAST("market_revenue_real" AS BIGINT) AS market_revenue_real,
    CAST("market_passenger_miles_flown" AS BIGINT) AS market_passenger_miles_flown,
    CAST("average_market_fare_constant" AS BIGINT) AS average_market_fare_constant,
    CAST("market_revenue_constant" AS BIGINT) AS market_revenue_constant,
    CAST("average_market_yield_sm" AS DOUBLE) AS average_market_yield_sm,
    CAST("average_market_miles_flown" AS DOUBLE) AS average_market_miles_flown,
    CAST("year_quarter" AS TIMESTAMP) AS year_quarter
FROM "u-s-department-of-transportation-h77j-murt"
