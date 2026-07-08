SELECT
    StationID                                AS station_id,
    WXID                                     AS wx_id,
    StationName                              AS station_name,
    NESSID                                   AS ness_id,
    NWSID                                    AS nws_id,
    TRY_CAST(Elevation AS INTEGER)           AS elevation_ft,
    TRY_CAST(Latitude AS DOUBLE)             AS latitude,
    TRY_CAST(Longitude AS DOUBLE)            AS longitude,
    State                                    AS state,
    County                                   AS county,
    Agency                                   AS agency,
    Region                                   AS region,
    Unit                                     AS unit,
    SubUnit                                  AS subunit,
    Status                                   AS status,
    CASE WHEN epoch_ms(TRY_CAST(ObservedDate AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(ObservedDate AS BIGINT)) END                    AS observed_at
FROM "nifc-29185087b4594a35abe059cbdbf97ee4-1"
