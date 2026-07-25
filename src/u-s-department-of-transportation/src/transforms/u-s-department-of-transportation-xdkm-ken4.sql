-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("date" AS TIMESTAMP) AS date,
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lon" AS DOUBLE) AS lon,
    CAST("spd" AS DOUBLE) AS spd,
    CAST("blind_turn" AS BIGINT) AS blind_turn,
    CAST("constrained_tunnel" AS BIGINT) AS constrained_tunnel,
    CAST("narrow" AS BIGINT) AS narrow,
    CAST("slow_sign" AS BIGINT) AS slow_sign,
    CAST("trail_hazards" AS BIGINT) AS trail_hazards,
    CAST("trail_junction" AS BIGINT) AS trail_junction,
    CAST("vehicle_conflict_point" AS BIGINT) AS vehicle_conflict_point,
    CAST("walk_bike_sign" AS BIGINT) AS walk_bike_sign,
    CAST("eb" AS BIGINT) AS eb,
    CAST("uphill" AS BIGINT) AS uphill,
    CAST("downhill" AS BIGINT) AS downhill,
    CAST("passing" AS BIGINT) AS passing,
    CAST("participantid" AS BIGINT) AS participantid,
    CAST("age" AS BIGINT) AS age,
    "sex",
    "bike_type",
    CAST("ebike_class" AS BIGINT) AS ebike_class
FROM "u-s-department-of-transportation-xdkm-ken4"
