SELECT
    ip_address,
    TRY_CAST(port AS INTEGER)           AS port,
    status,
    hostname,
    TRY_CAST(as_number AS BIGINT)       AS as_number,
    as_name,
    country,
    TRY_CAST(first_seen AS TIMESTAMP)   AS first_seen,
    TRY_CAST(last_online AS DATE)       AS last_online,
    malware
FROM "abuse-ch-feodotracker-c2"
WHERE ip_address IS NOT NULL
