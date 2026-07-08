SELECT
    CAST(t AS INTEGER)                        AS year,
    CAST(i AS INTEGER)                        AS exporter_iso,
    CAST(j AS INTEGER)                        AS importer_iso,
    LPAD(CAST(k AS VARCHAR), 6, '0')          AS product_hs92,
    TRY_CAST(v AS DOUBLE)                     AS value_kusd,
    TRY_CAST(q AS DOUBLE)                     AS quantity_t
FROM "cepii-baci"
WHERE t IS NOT NULL
