SELECT station_id, from_date, to_date, height_m, latitude, longitude, name, bundesland
FROM "dwd-stations"
WHERE station_id IS NOT NULL
