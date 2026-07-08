SELECT station_id, CAST(t AS TIMESTAMP) AS occurred_at, value AS flow_m3s FROM "national-river-flow-archive-pot-flow" WHERE value IS NOT NULL
