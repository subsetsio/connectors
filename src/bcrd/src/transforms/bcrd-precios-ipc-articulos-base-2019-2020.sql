SELECT
    file,
    sheet,
    CAST("row" AS INTEGER) AS row_idx,
    CAST("col" AS INTEGER) AS col_idx,
    row_label,
    value         AS value_text,
    CAST(num AS DOUBLE) AS value_num
FROM "bcrd-precios-ipc-articulos-base-2019-2020"
WHERE value IS NOT NULL
