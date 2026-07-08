SELECT
    project,
    CAST(date AS DATE) AS date,
    "net_bytes_diff"
FROM "wikipedia-bytes-difference-net"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "net_bytes_diff" IS NOT NULL
