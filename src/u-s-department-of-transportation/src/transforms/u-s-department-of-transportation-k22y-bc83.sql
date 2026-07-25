-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "uace_code",
    "uza_name",
    "uza_shortname",
    CAST("population_num" AS BIGINT) AS population_num,
    "rail_bus_ferry",
    CAST("month_year" AS TIMESTAMP) AS month_year,
    "event_type",
    "metric",
    CAST("value" AS BIGINT) AS value,
    CAST("ridership" AS BIGINT) AS ridership,
    CAST("vehicle_revenue_miles" AS BIGINT) AS vehicle_revenue_miles,
    CAST("metric_ridership_rate" AS DOUBLE) AS metric_ridership_rate,
    CAST("metric_vehicle_revenue_miles" AS DOUBLE) AS metric_vehicle_revenue_miles,
    CAST("cost_pp" AS DOUBLE) AS cost_pp,
    CAST("perc_ada" AS DOUBLE) AS perc_ada,
    CAST("ridership_6mo_avg" AS DOUBLE) AS ridership_6mo_avg,
    CAST("vehicle_revenue_hours_6mo_avg" AS DOUBLE) AS vehicle_revenue_hours_6mo_avg,
    CAST("vehicle_revenue_miles_6mo_avg" AS DOUBLE) AS vehicle_revenue_miles_6mo_avg,
    CAST("value_6mo_avg" AS DOUBLE) AS value_6mo_avg,
    CAST("metric_ridership_6mo_avg_rate" AS DOUBLE) AS metric_ridership_6mo_avg_rate,
    CAST("metric_vehicle_revenue_hours_6mo_avg_rate" AS DOUBLE) AS metric_vehicle_revenue_hours_6mo_avg_rate,
    CAST("metric_vehicle_revenue_miles_6mo_avg_rate" AS DOUBLE) AS metric_vehicle_revenue_miles_6mo_avg_rate,
    CAST("year" AS TIMESTAMP) AS year
FROM "u-s-department-of-transportation-k22y-bc83"
