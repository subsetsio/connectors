SELECT
        office,
        origin,
        indicator_id,
        indicator,
        report_type,
        CAST(year AS INTEGER)          AS year,
        breakdown_index,
        CAST(value AS DOUBLE)          AS value
    FROM "wipo-country-profiles"
    WHERE value IS NOT NULL
