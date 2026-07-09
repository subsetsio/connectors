SELECT
    CAST(indicator_id AS INTEGER)  AS indicator_id,
    module,
    tab,
    label,
    report_types
FROM "wipo-indicators"
WHERE indicator_id IS NOT NULL
