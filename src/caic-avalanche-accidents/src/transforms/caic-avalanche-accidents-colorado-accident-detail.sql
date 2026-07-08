SELECT
    acc_id,
    acc_date                               AS accident_date,
    EXTRACT(year FROM acc_date)::INTEGER   AS year,
    acc_activity                           AS activity,
    travel_mode,
    acc_location                           AS location,
    acc_lat                                AS latitude,
    acc_lon                                AS longitude,
    CAST(acc_no_caught AS INTEGER)         AS number_caught,
    CAST(acc_no_buried AS INTEGER)         AS number_buried,
    CAST(acc_no_killed AS INTEGER)         AS number_killed,
    atype                                  AS avalanche_type,
    aspect,
    elevation                              AS elevation_ft,
    slope                                  AS slope_angle,
    rscale                                 AS relative_size,
    dscale                                 AS destructive_size,
    trigger,
    trig_desc                              AS trigger_description,
    surface                                AS bed_surface,
    report                                 AS report_url
FROM "caic-avalanche-accidents-colorado-accident-detail"
WHERE acc_date IS NOT NULL
