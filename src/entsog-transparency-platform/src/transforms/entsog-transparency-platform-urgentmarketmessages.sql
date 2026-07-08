WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-urgentmarketmessages"
)
SELECT
    id,
    messageId                                          AS message_id,
    marketParticipantName                              AS market_participant_name,
    messageType                                        AS message_type,
    eventType                                          AS event_type,
    eventStatus                                        AS event_status,
    TRY_CAST(publicationDateTime AS TIMESTAMP)         AS publication_date,
    TRY_CAST(eventStart AS TIMESTAMP)                  AS event_start,
    TRY_CAST(eventStop AS TIMESTAMP)                   AS event_stop,
    balancingZoneName                                  AS balancing_zone_name,
    TRY_CAST(NULLIF(unavailableCapacity, '') AS DOUBLE) AS unavailable_capacity,
    TRY_CAST(NULLIF(availableCapacity, '') AS DOUBLE)   AS available_capacity,
    TRY_CAST(NULLIF(technicalCapacity, '') AS DOUBLE)   AS technical_capacity,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)          AS last_update
FROM ranked
WHERE rn = 1
