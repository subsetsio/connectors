SELECT DISTINCT
    sistema, proceso, clv_zona_reserva AS reserve_zone,
    tipo_res AS reserve_type,
    CAST(fecha AS DATE) AS date, hora AS hour,
    pres
FROM "cenace-psc"
WHERE fecha IS NOT NULL AND hora IS NOT NULL
