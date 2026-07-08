SELECT
    registry,
    NULLIF(country, '')                       AS country,
    type,
    start,
    TRY_CAST(value AS BIGINT)                 AS value,
    TRY_STRPTIME(NULLIF(date, ''), '%Y%m%d')::DATE AS allocation_date,
    status,
    opaque_id
FROM "ripe-ncc-rir-allocations"
WHERE type IN ('ipv4', 'ipv6', 'asn')
