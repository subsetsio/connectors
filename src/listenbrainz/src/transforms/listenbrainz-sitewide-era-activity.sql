SELECT
    range,
    CAST(year AS INTEGER) AS year,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(last_updated) AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-era-activity"
WHERE year IS NOT NULL AND listen_count IS NOT NULL
  -- drop garbage MusicBrainz release-year tags (e.g. 2913); recorded
  -- music spans ~1860 to the near future.
  AND year BETWEEN 1860 AND CAST(EXTRACT(YEAR FROM current_date) AS INTEGER) + 1
