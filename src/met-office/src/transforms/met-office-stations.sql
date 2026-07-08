SELECT
    station,
    name,
    lat,
    lon,
    CAST(altitude_m AS INTEGER) AS altitude_m,
    CAST(start_year AS INTEGER) AS start_year,
    CAST(end_year AS INTEGER)   AS end_year,
    location
FROM "met-office-stations"
