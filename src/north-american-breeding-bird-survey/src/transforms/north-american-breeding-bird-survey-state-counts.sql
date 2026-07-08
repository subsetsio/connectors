SELECT
    TRY_CAST(TRIM(RouteDataID) AS BIGINT) AS route_data_id,
    TRY_CAST(TRIM(CountryNum) AS INTEGER) AS country_num,
    TRIM(StateNum)                        AS state_num,
    TRIM(Route)                           AS route,
    TRIM(RPID)                            AS rpid,
    TRY_CAST(TRIM(Year) AS INTEGER)       AS year,
    TRY_CAST(TRIM(AOU) AS INTEGER) AS aou,
    TRY_CAST(TRIM("Count10") AS INTEGER) AS count10,
        TRY_CAST(TRIM("Count20") AS INTEGER) AS count20,
        TRY_CAST(TRIM("Count30") AS INTEGER) AS count30,
        TRY_CAST(TRIM("Count40") AS INTEGER) AS count40,
        TRY_CAST(TRIM("Count50") AS INTEGER) AS count50,
        TRY_CAST(TRIM("StopTotal") AS INTEGER) AS stoptotal,
        TRY_CAST(TRIM("SpeciesTotal") AS INTEGER) AS speciestotal
FROM "north-american-breeding-bird-survey-state-counts"
