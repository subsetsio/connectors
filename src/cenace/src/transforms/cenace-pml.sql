SELECT DISTINCT
    sistema, proceso, clv_nodo AS node,
    CAST(fecha AS DATE) AS date, hora AS hour,
    pml, pml_ene, pml_per, pml_cng
FROM "cenace-pml"
WHERE fecha IS NOT NULL AND hora IS NOT NULL
