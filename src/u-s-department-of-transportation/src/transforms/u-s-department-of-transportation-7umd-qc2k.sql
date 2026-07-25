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
    CAST("most_used_vessel_id" AS BIGINT) AS most_used_vessel_id,
    "vessel_id1",
    "vessel_id2",
    "vessel_id3",
    "vessel_id4",
    "vessel_id5",
    "vessel_id6",
    "vessel_id7",
    "vessel_id8",
    "vessel_id9",
    "vessel_id10",
    "vessel_id11",
    "vessel_id12",
    "vessel_id13",
    "vessel_id14",
    "vessel_id15",
    "vessel_id16",
    "vessel_id17",
    "vessel_id18",
    "vessel_id19",
    "vessel_id20",
    CAST("passengers" AS BIGINT) AS passengers,
    CAST("vehicles" AS BIGINT) AS vehicles,
    CAST("avg_daily_brd_pax" AS BIGINT) AS avg_daily_brd_pax,
    CAST("avg_daily_brd_veh" AS BIGINT) AS avg_daily_brd_veh,
    CAST("census_year" AS BIGINT) AS census_year
FROM "u-s-department-of-transportation-7umd-qc2k"
