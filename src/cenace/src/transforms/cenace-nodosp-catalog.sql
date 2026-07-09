SELECT DISTINCT
    sistema,
    centro_control_regional,
    zona_carga AS load_zone,
    clave AS node,
    nombre,
    nivel_tension_kv,
    zona_operacion_transmision,
    zona_distribucion,
    entidad_federativa,
    municipio,
    region_transmision
FROM "cenace-nodosp-catalog"
WHERE clave IS NOT NULL
