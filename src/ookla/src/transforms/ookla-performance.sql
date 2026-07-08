SELECT
    quadkey,
    connection_type,
    CAST(year AS INTEGER)    AS year,
    CAST(quarter AS INTEGER) AS quarter,
    make_date(year, (quarter - 1) * 3 + 1, 1) AS period_start,
    avg_d_kbps      AS avg_download_kbps,
    avg_u_kbps      AS avg_upload_kbps,
    avg_lat_ms      AS avg_latency_ms,
    avg_lat_down_ms AS avg_latency_download_ms,
    avg_lat_up_ms   AS avg_latency_upload_ms,
    tests,
    devices,
    tile_x,
    tile_y
FROM "ookla-performance"
WHERE quadkey IS NOT NULL
