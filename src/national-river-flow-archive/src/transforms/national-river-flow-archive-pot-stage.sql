SELECT station_id, CAST(t AS TIMESTAMP) AS occurred_at, value AS stage_m FROM "national-river-flow-archive-pot-stage" WHERE value IS NOT NULL
