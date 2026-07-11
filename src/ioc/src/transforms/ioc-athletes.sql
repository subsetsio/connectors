SELECT
    CAST(edition AS VARCHAR) AS edition,
    CAST(games AS VARCHAR) AS games,
    CAST(athlete_code AS VARCHAR) AS athlete_code,
    CAST(archive_timestamp AS VARCHAR) AS archive_timestamp,
    CAST(source_url AS VARCHAR) AS source_url,
    CAST(to_json(payload) AS VARCHAR) AS payload_json
FROM "ioc-athletes"
WHERE athlete_code IS NOT NULL

