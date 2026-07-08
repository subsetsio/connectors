SELECT
    day_of_year,
    hemisphere,
    average_extent_million_km2,
    std_deviation_million_km2,
    pctl_10_million_km2,
    pctl_25_million_km2,
    pctl_50_million_km2,
    pctl_75_million_km2,
    pctl_90_million_km2
FROM "nsidc-sea-ice-extent-daily-climatology"
ORDER BY hemisphere, day_of_year
