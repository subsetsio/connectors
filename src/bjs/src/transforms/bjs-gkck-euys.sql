SELECT * REPLACE (
    TRY_CAST(year AS INTEGER) AS year,
    TRY_CAST(yearq AS DOUBLE) AS yearq,
    TRY_CAST(wgtviccy AS DOUBLE) AS wgtviccy,
    TRY_CAST(newwgt AS DOUBLE) AS newwgt
)
FROM "bjs-gkck-euys"
