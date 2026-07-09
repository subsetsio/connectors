SELECT
        indicator_id,
        indicator,
        ip_right,
        office,
        origin,
        CAST(year AS INTEGER)          AS year,
        breakdown_index,
        CAST(value AS DOUBLE)          AS value
    FROM "wipo-key-indicators"
    WHERE value IS NOT NULL
