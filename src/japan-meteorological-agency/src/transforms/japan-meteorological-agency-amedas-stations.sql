SELECT
    station_id, type AS station_type, elems,
    lat, lon, alt,
    name_ja, name_kana, name_en
FROM "japan-meteorological-agency-amedas-stations"
WHERE station_id IS NOT NULL
