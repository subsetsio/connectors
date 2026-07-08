SELECT DISTINCT
    sistema, proceso, zona_carga AS load_zone,
    CAST(fecha AS DATE) AS date, hora AS hour,
    pz, pz_ene, pz_per, pz_cng
FROM "cenace-pend"
WHERE fecha IS NOT NULL AND hora IS NOT NULL
