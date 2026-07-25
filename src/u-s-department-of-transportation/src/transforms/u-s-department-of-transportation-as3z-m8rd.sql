-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("operator_id" AS BIGINT) AS operator_id,
    CAST("segment_id" AS BIGINT) AS segment_id,
    CAST("segment_length" AS DOUBLE) AS segment_length,
    CAST("average_trip_time" AS BIGINT) AS average_trip_time,
    "segment_season_start",
    "segment_season_end",
    CAST("trips_per_year" AS BIGINT) AS trips_per_year,
    CAST("route_rates_regulated" AS BOOLEAN) AS route_rates_regulated,
    "route_rate_regulator",
    "most_used_vessel_id",
    CAST("vessel_id1" AS BIGINT) AS vessel_id1,
    CAST("vessel_id2" AS BIGINT) AS vessel_id2,
    CAST("vessel_id3" AS BIGINT) AS vessel_id3,
    CAST("vessel_id4" AS BIGINT) AS vessel_id4,
    CAST("vessel_id5" AS BIGINT) AS vessel_id5,
    CAST("vessel_id6" AS BIGINT) AS vessel_id6,
    CAST("vessel_id7" AS BIGINT) AS vessel_id7,
    CAST("vessel_id8" AS BIGINT) AS vessel_id8,
    CAST("vessel_id9" AS BIGINT) AS vessel_id9,
    CAST("vessel_id10" AS BIGINT) AS vessel_id10,
    CAST("vessel_id11" AS BIGINT) AS vessel_id11,
    CAST("vessel_id12" AS BIGINT) AS vessel_id12,
    CAST("vessel_id13" AS BIGINT) AS vessel_id13,
    CAST("passengers" AS BIGINT) AS passengers,
    CAST("vehicles" AS BIGINT) AS vehicles,
    CAST("avg_daily_brd_pax" AS BIGINT) AS avg_daily_brd_pax,
    CAST("avg_daily_brd_veh" AS BIGINT) AS avg_daily_brd_veh,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-as3z-m8rd"
