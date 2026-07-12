-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One collision can have multiple casualty rows, so aggregating this table by collision attributes counts casualties unless deduplicated to the collision grain.
SELECT
    "collision_index",
    "collision_year",
    "collision_ref_no",
    "vehicle_reference",
    "casualty_reference",
    "casualty_class",
    "sex_of_casualty",
    "age_of_casualty",
    "age_band_of_casualty",
    "casualty_severity",
    "pedestrian_location",
    "pedestrian_movement",
    "car_passenger",
    "bus_or_coach_passenger",
    "pedestrian_road_maintenance_worker",
    "casualty_type",
    "casualty_imd_decile",
    CAST("lsoa_of_casualty" AS VARCHAR) AS "lsoa_of_casualty",
    "enhanced_casualty_severity",
    "casualty_injury_based",
    CAST("casualty_adjusted_severity_serious" AS DOUBLE) AS "casualty_adjusted_severity_serious",
    CAST("casualty_adjusted_severity_slight" AS DOUBLE) AS "casualty_adjusted_severity_slight",
    "casualty_distance_banding"
FROM "stats19-casualties"
