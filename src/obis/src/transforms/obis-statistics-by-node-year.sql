SELECT
    nodeid,
    node_name,
    node_type,
    CAST(year AS INTEGER) AS year,
    CAST(records AS BIGINT) AS records
FROM "obis-statistics-by-node-year"
WHERE nodeid IS NOT NULL AND year IS NOT NULL
