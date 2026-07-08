SELECT
    sheet,
    CAST(row_index AS INTEGER) AS row_index,
    CAST(col_index AS INTEGER) AS col_index,
    row_label,
    col_header,
    CAST(value AS DOUBLE)      AS value,
    value_text
FROM "banco-central-del-ecuador-documentos-informacioneconomica-cuentasnacionales-anuales-bam-mei-2018-2022"
WHERE value IS NOT NULL OR value_text IS NOT NULL
