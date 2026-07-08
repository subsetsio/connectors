SELECT
    UniqueFireIdentifier                     AS unique_fire_id,
    IncidentName                             AS incident_name,
    TRY_CAST(CalendarYear AS INTEGER)        AS calendar_year,
    CASE WHEN epoch_ms(TRY_CAST(FireDiscoveryDateTime AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(FireDiscoveryDateTime AS BIGINT)) END           AS fire_discovery_at,
    CASE WHEN epoch_ms(TRY_CAST(ContainmentDateTime AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(ContainmentDateTime AS BIGINT)) END             AS containment_at,
    CASE WHEN epoch_ms(TRY_CAST(FireOutDateTime AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(FireOutDateTime AS BIGINT)) END                 AS fire_out_at,
    TRY_CAST(IncidentSize AS DOUBLE)         AS incident_size_acres,
    IncidentTypeCategory                     AS incident_type_category,
    GACC                                     AS gacc,
    POOState                                 AS state,
    POOCounty                                AS county,
    POOJurisdictionalAgency                  AS jurisdictional_agency,
    POOProtectingAgency                      AS protecting_agency,
    TRY_CAST(InitialLatitude AS DOUBLE)      AS latitude,
    TRY_CAST(InitialLongitude AS DOUBLE)     AS longitude,
    Status                                   AS status,
    FireCode                                 AS fire_code
FROM "nifc-60a94840152b4a89bec467a9f052f135-0"
