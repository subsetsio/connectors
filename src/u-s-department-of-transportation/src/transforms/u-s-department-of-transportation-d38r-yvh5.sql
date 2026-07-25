-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("operator_id" AS BIGINT) AS operator_id,
    CAST("segment_id" AS BIGINT) AS segment_id,
    CAST("seg_length" AS DOUBLE) AS seg_length,
    CAST("average_trip_time" AS BIGINT) AS average_trip_time,
    "segment_season_start",
    "segment_season_end",
    CAST("trips_per_year" AS BIGINT) AS trips_per_year,
    CAST("route_rates_regulated" AS BIGINT) AS route_rates_regulated,
    "route_rate_regulator",
    CAST("most_used_vessel_id" AS BIGINT) AS most_used_vessel_id,
    CAST("vessel1_id" AS BIGINT) AS vessel1_id,
    CAST("vessel2_id" AS BIGINT) AS vessel2_id,
    CAST("vessel3_id" AS BIGINT) AS vessel3_id,
    CAST("vessel4_id" AS BIGINT) AS vessel4_id,
    CAST("vessel5_id" AS BIGINT) AS vessel5_id,
    CAST("vessel6_id" AS BIGINT) AS vessel6_id,
    CAST("vessel7_id" AS BIGINT) AS vessel7_id,
    CAST("vessel8_id" AS BIGINT) AS vessel8_id,
    CAST("vessel9_id" AS BIGINT) AS vessel9_id,
    CAST("vessel10_id" AS BIGINT) AS vessel10_id,
    CAST("vessel11_id" AS BIGINT) AS vessel11_id,
    CAST("vessel12_id" AS BIGINT) AS vessel12_id,
    CAST("vessel13_id" AS BIGINT) AS vessel13_id,
    CAST("vessel14_id" AS BIGINT) AS vessel14_id,
    CAST("vessel15_id" AS BIGINT) AS vessel15_id,
    CAST("vessel16_id" AS BIGINT) AS vessel16_id,
    CAST("vessel17_id" AS BIGINT) AS vessel17_id,
    CAST("passengers" AS BIGINT) AS passengers,
    CAST("vehicles" AS BIGINT) AS vehicles,
    CAST("avg_daily_brd_pax" AS BIGINT) AS avg_daily_brd_pax,
    CAST("avg_daily_brd_veh" AS BIGINT) AS avg_daily_brd_veh,
    CAST("survey_year" AS BIGINT) AS survey_year
FROM "u-s-department-of-transportation-d38r-yvh5"
