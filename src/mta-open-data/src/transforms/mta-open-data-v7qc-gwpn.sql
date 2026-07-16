-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "from_date",
    "to_date",
    "remote_station_id",
    "station",
    "full_fare",
    "senior_citizen_disabled",
    "_7_day_ada_farecard_access_system_unlimited" AS "7_day_ada_farecard_access_system_unlimited",
    "_30_day_ada_farecard_access_reduced_fare_media_unlimited" AS "30_day_ada_farecard_access_reduced_fare_media_unlimited",
    "joint_rail_road_ticket",
    "_7_day_unlimited" AS "7_day_unlimited",
    "_30_day_unlimited" AS "30_day_unlimited",
    "_14_day_reduced_fare_media_unlimited" AS "14_day_reduced_fare_media_unlimited",
    "_1_day_unlimited" AS "1_day_unlimited",
    "_14_day_unlimited" AS "14_day_unlimited",
    "_7_day_express_bus_pass" AS "7_day_express_bus_pass",
    "transitcheck",
    "long_island_bus_special_senior",
    "reduced_fare_2_trip",
    "rail_road_unlimited_no_trade",
    "transitcheck_annual",
    "mail_and_ride_easypay_express",
    "mail_and_ride_easypay_unlimited",
    "path_2_trip",
    "airtrain_full_fare",
    "airtrain_30_day_unlimited",
    "airtrain_10_trip",
    "airtrain_monthly",
    "student",
    "nice_2_trip",
    "cuny_120_day",
    "cuny_60_day",
    "fair_fares_pay_per_ride",
    "fair_fares_7_day_unlimited",
    "fair_fares_30_day_unlimited"
FROM "mta-open-data-v7qc-gwpn"
