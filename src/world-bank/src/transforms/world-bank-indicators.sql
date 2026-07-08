SELECT
    id                          AS indicator_code,
    name,
    source_id,
    NULLIF(source_name, '')     AS source_name,
    NULLIF(source_note, '')     AS definition,
    NULLIF(source_organization, '') AS source_organization,
    NULLIF(topic_names, '')     AS topics
FROM "world-bank-indicators"
WHERE id IS NOT NULL
