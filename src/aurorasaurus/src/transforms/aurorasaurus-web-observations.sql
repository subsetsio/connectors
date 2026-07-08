SELECT
    TRY_CAST(id AS BIGINT)                  AS report_id,
    CAST(timestamp AS TIMESTAMP)            AS observed_at,
    TRY_CAST(location.latitude  AS DOUBLE)  AS latitude,
    TRY_CAST(location.longitude AS DOUBLE)  AS longitude,
    address_country                         AS country,
    address_state                           AS state,
    CAST(see_aurora AS BOOLEAN)             AS saw_aurora,
    sky                                     AS sky,
    array_to_string(colors, ',')            AS colors,
    array_to_string(types, ',')             AS types,
    activities                              AS activities,
    height                                  AS height,
    comment                                 AS comment,
    TRY_CAST(time_start AS TIMESTAMP)       AS report_time_start,
    TRY_CAST(time_end   AS TIMESTAMP)       AS report_time_end
FROM "aurorasaurus-web-observations"
WHERE id IS NOT NULL
