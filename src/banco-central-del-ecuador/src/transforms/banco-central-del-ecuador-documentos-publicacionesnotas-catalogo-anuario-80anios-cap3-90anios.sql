SELECT
    sheet,
    CAST(row_index AS INTEGER) AS row_index,
    CAST(col_index AS INTEGER) AS col_index,
    row_label,
    col_header,
    CAST(value AS DOUBLE)      AS value,
    value_text
FROM "banco-central-del-ecuador-documentos-publicacionesnotas-catalogo-anuario-80anios-cap3-90anios"
WHERE value IS NOT NULL OR value_text IS NOT NULL
