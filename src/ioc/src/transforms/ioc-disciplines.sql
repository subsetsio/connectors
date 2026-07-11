SELECT
    CAST(edition AS VARCHAR) AS edition,
    CAST(games AS VARCHAR) AS games,
    CAST(archive_timestamp AS VARCHAR) AS archive_timestamp,
    CAST(source_url AS VARCHAR) AS source_url,
    CAST(to_json(payload) AS VARCHAR) AS payload_json
FROM "ioc-disciplines"

