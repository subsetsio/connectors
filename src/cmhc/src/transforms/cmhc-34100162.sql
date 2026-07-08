SELECT
    CAST("REF_DATE" AS VARCHAR) AS ref_date,
    "GEO"      AS geo,
    * EXCLUDE ("REF_DATE", "GEO", "UOM", "STATUS", "VALUE", "DGUID","UOM_ID","SCALAR_FACTOR","SCALAR_ID","VECTOR","COORDINATE","SYMBOL","TERMINATED","DECIMALS"),
    "UOM"      AS uom,
    "STATUS"   AS status,
    TRY_CAST("VALUE" AS DOUBLE) AS value
FROM "cmhc-34100162"
WHERE TRY_CAST("VALUE" AS DOUBLE) IS NOT NULL
  -- -999 is a StatCan missing-value sentinel (e.g. vacancy "Rate" = -999,
  -- which is impossible), not a real observation; drop it.
  AND TRY_CAST("VALUE" AS DOUBLE) <> -999
