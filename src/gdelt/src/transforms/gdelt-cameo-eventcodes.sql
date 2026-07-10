SELECT
    CAST(event_code AS VARCHAR) AS event_code,
    CAST(event_description AS VARCHAR) AS event_description
FROM "gdelt-cameo-eventcodes"
