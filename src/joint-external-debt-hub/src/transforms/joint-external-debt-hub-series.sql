SELECT
    series_code,
    series_name,
    unit,
    source_id,
    source_name,
    source_note,
    source_organization,
    topics_json
FROM "joint-external-debt-hub-series"
WHERE series_code IS NOT NULL

