SELECT
    TRY_CAST(VehicleId AS BIGINT)                  AS vehicle_id,
    TRY_CAST(ModelYear AS INTEGER)                 AS model_year,
    NULLIF(TRIM(Make), '')                         AS make,
    NULLIF(TRIM(Model), '')                        AS model,
    NULLIF(TRIM(VehicleDescription), '')           AS vehicle_description,
    NULLIF(TRIM(OverallRating), '')                AS overall_rating,
    NULLIF(TRIM(OverallFrontCrashRating), '')      AS overall_front_crash_rating,
    NULLIF(TRIM(OverallSideCrashRating), '')       AS overall_side_crash_rating,
    NULLIF(TRIM(RolloverRating), '')               AS rollover_rating,
    TRY_CAST(RolloverPossibility AS DOUBLE)        AS rollover_possibility,
    NULLIF(TRIM(FrontCrashDriversideRating), '')   AS front_crash_driver_rating,
    NULLIF(TRIM(FrontCrashPassengersideRating), '') AS front_crash_passenger_rating,
    NULLIF(TRIM(SideCrashDriversideRating), '')    AS side_crash_driver_rating,
    NULLIF(TRIM(SideCrashPassengersideRating), '') AS side_crash_passenger_rating,
    NULLIF(TRIM(SidePoleCrashRating), '')          AS side_pole_crash_rating,
    NULLIF(TRIM(NHTSAElectronicStabilityControl), '') AS electronic_stability_control,
    NULLIF(TRIM(NHTSAForwardCollisionWarning), '') AS forward_collision_warning,
    NULLIF(TRIM(NHTSALaneDepartureWarning), '')    AS lane_departure_warning,
    TRY_CAST(RecallsCount AS INTEGER)              AS recalls_count,
    TRY_CAST(ComplaintsCount AS INTEGER)           AS complaints_count,
    TRY_CAST(InvestigationCount AS INTEGER)        AS investigations_count
FROM "nhtsa-safety-ratings"
WHERE VehicleId IS NOT NULL
