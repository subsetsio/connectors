SELECT * REPLACE (
    TRY_CAST(year AS INTEGER) AS year,
    TRY_CAST(yearq AS DOUBLE) AS yearq,
    TRY_CAST(wgthhcy AS DOUBLE) AS wgthhcy
)
FROM "bjs-ya4e-n9zp"
