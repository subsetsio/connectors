SELECT
    product_id,
    file_name,
    url,
    variable,
    domain,
    grid,
    description,
    format,
    CAST(http_status AS INTEGER) AS http_status,
    CAST(content_length_bytes AS BIGINT) AS content_length_bytes,
    CAST(last_modified AS TIMESTAMP) AS last_modified,
    etag,
    CAST(checked_at AS TIMESTAMP) AS checked_at
FROM "berkeley-earth-gridded-temperature"
