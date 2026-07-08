SELECT
    TRY_CAST(first_seen_utc AS TIMESTAMP)    AS first_seen_utc,
    TRY_CAST(ioc_id AS BIGINT)               AS ioc_id,
    ioc_value,
    ioc_type,
    threat_type,
    fk_malware,
    malware_alias,
    malware_printable,
    TRY_CAST(last_seen_utc AS TIMESTAMP)     AS last_seen_utc,
    TRY_CAST(confidence_level AS INTEGER)    AS confidence_level,
    is_compromised,
    reference,
    tags,
    anonymous,
    reporter
FROM "abuse-ch-threatfox-iocs"
WHERE ioc_id IS NOT NULL
