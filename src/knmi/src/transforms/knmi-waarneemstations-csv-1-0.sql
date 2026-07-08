SELECT CAST(station_id AS INTEGER) AS station_id,
       wsi, location, station_type,
       TRY_CAST(start_date AS DATE) AS start_date,
       TRY_CAST(stop_date AS DATE) AS stop_date,
       CAST(height_m AS DOUBLE) AS height_m,
       CAST(latitude AS DOUBLE) AS latitude,
       CAST(longitude AS DOUBLE) AS longitude,
       CAST(pos_x AS DOUBLE) AS pos_x,
       CAST(pos_y AS DOUBLE) AS pos_y
FROM "knmi-waarneemstations-csv-1-0"
WHERE station_id IS NOT NULL
