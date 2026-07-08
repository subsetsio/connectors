SELECT
    CAST(STATIONS_ID AS INTEGER) AS station_id,
    strptime(trim(CAST(MESS_DATUM AS VARCHAR)), '%Y%m%d')::DATE AS date,
    nullif(
        TRY_CAST(
            COLUMNS(c -> c NOT IN ('STATIONS_ID', 'MESS_DATUM', 'MESS_DATUM_BEGINN', 'MESS_DATUM_ENDE', 'eor') AND NOT starts_with(c, 'QN')) AS DOUBLE
        ),
        -999
    )
FROM "dwd-obs-daily-solar"
WHERE TRY_CAST(STATIONS_ID AS INTEGER) IS NOT NULL
  AND strptime(trim(CAST(MESS_DATUM AS VARCHAR)), '%Y%m%d') IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY CAST(STATIONS_ID AS INTEGER),
                 strptime(trim(CAST(MESS_DATUM AS VARCHAR)), '%Y%m%d')::DATE
    ORDER BY MESS_DATUM
) = 1
