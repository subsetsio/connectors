-- CNEOS fireball events. Fold the hemisphere flags into signed coordinates
-- (S/W negative); energies stay in the source's units (see contract).
SELECT
    CAST("date" AS TIMESTAMP) AS event_time,
    CAST("energy" AS DOUBLE) AS radiated_energy_e10j,
    CAST("impact_e" AS DOUBLE) AS impact_energy_kt,
    CAST("lat" AS DOUBLE) * (CASE WHEN "lat_dir" = 'S' THEN -1 ELSE 1 END) AS latitude,
    CAST("lon" AS DOUBLE) * (CASE WHEN "lon_dir" = 'W' THEN -1 ELSE 1 END) AS longitude,
    CAST("alt" AS DOUBLE) AS altitude_km,
    CAST("vel" AS DOUBLE) AS velocity_kms
FROM "nasa-fireball"
