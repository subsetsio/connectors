SELECT * REPLACE (
    TRY_CAST(year AS INTEGER) AS year,
    TRY_CAST(yearq AS DOUBLE) AS yearq,
    TRY_CAST(wgtpercy AS DOUBLE) AS wgtpercy
)
FROM "bjs-r4j4-fdwx"
