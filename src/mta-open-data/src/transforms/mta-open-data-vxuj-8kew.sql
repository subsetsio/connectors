-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "subways_total_estimated_ridership",
    "subways_of_comparable_pre_pandemic_day",
    "buses_total_estimated_ridersip",
    "buses_of_comparable_pre_pandemic_day",
    "lirr_total_estimated_ridership",
    "lirr_of_comparable_pre_pandemic_day",
    "metro_north_total_estimated_ridership",
    "metro_north_of_comparable_pre_pandemic_day",
    "access_a_ride_total_scheduled_trips",
    "access_a_ride_of_comparable_pre_pandemic_day",
    "bridges_and_tunnels_total_traffic",
    "bridges_and_tunnels_of_comparable_pre_pandemic_day",
    "staten_island_railway_total_estimated_ridership",
    "staten_island_railway_of_comparable_pre_pandemic_day"
FROM "mta-open-data-vxuj-8kew"
