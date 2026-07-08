-- gain/loss are returned by the API but always null on this endpoint; dropped.
SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    CAST(year AS INTEGER)      AS year,
    CAST(net_change AS DOUBLE) AS net_change
FROM "global-mangrove-watch-net-change"
WHERE net_change IS NOT NULL
