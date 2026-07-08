SELECT
    * EXCLUDE (date_received, date_sent_to_company, complaint_id),
    TRY_CAST(date_received AS DATE)        AS date_received,
    TRY_CAST(date_sent_to_company AS DATE) AS date_sent_to_company,
    TRY_CAST(complaint_id AS BIGINT)       AS complaint_id
FROM "cfpb-consumer-complaints"
