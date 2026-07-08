SELECT
    TRY_CAST(TRIM(CountryNum) AS INTEGER)        AS country_num,
    TRIM(StateNum)                               AS state_num,
    TRIM(Route)                                  AS route,
    TRIM(RouteName)                              AS route_name,
    TRY_CAST(TRIM(Active) AS INTEGER)            AS active,
    TRY_CAST(TRIM(Latitude) AS DOUBLE)           AS latitude,
    TRY_CAST(TRIM(Longitude) AS DOUBLE)          AS longitude,
    TRY_CAST(TRIM(Stratum) AS INTEGER)           AS stratum,
    TRY_CAST(TRIM(BCR) AS INTEGER)               AS bcr,
    TRY_CAST(TRIM(RouteTypeID) AS INTEGER)       AS route_type_id,
    TRY_CAST(TRIM(RouteTypeDetailID) AS INTEGER) AS route_type_detail_id
FROM "north-american-breeding-bird-survey-routes"
