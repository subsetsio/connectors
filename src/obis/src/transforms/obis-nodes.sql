SELECT
    nodeid,
    node_name,
    description,
    theme,
    node_type,
    CAST(lon AS DOUBLE) AS lon,
    CAST(lat AS DOUBLE) AS lat,
    CAST(url_count AS INTEGER) AS url_count,
    CAST(feed_count AS INTEGER) AS feed_count,
    CAST(contact_count AS INTEGER) AS contact_count
FROM "obis-nodes"
WHERE nodeid IS NOT NULL
