SELECT
    codigo_indicador,
    nombre_indicador,
    nombre_indicador_en,
    tema,
    tema_raiz,
    ambito_departamental,
    ambito_provincial,
    ambito_distrital
FROM "inei-indicators"
WHERE codigo_indicador IS NOT NULL
  AND nombre_indicador IS NOT NULL
