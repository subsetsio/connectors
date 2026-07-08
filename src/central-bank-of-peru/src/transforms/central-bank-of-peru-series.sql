SELECT
    codigo_serie,
    NULLIF(categoria, '')          AS categoria,
    NULLIF(grupo, '')              AS grupo,
    NULLIF(nombre, '')             AS nombre,
    NULLIF(descripcion, '')        AS descripcion,
    NULLIF(geografia, '')          AS geografia,
    NULLIF(fuente, '')             AS fuente,
    NULLIF(frecuencia, '')         AS frecuencia,
    NULLIF(grupo_publicacion, '')  AS grupo_publicacion,
    NULLIF(area_publica, '')       AS area_publica,
    NULLIF(fecha_actualizacion,'') AS fecha_actualizacion,
    NULLIF(fecha_inicio, '')       AS fecha_inicio,
    NULLIF(fecha_fin, '')          AS fecha_fin
FROM "central-bank-of-peru-series"
WHERE codigo_serie IS NOT NULL AND codigo_serie <> ''
