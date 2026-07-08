SELECT
    entity_id,
    name,
    entity_type,
    region,
    continent,
    CAST(latest_year AS INTEGER)        AS latest_year,
    CAST(freedom_index AS DOUBLE)       AS freedom_index,
    freedom_status,
    CAST(freedom_rank AS INTEGER)       AS freedom_rank,
    CAST(prosperity_index AS DOUBLE)    AS prosperity_index,
    prosperity_status,
    CAST(prosperity_rank AS INTEGER)    AS prosperity_rank
FROM "atlantic-council-entities"
