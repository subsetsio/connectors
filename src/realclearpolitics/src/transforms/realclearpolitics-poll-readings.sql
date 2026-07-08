SELECT
    CAST(race_id AS BIGINT)                         AS race_id,
    CAST(race_title AS VARCHAR)                     AS race_title,
    CAST(office AS VARCHAR)                         AS office,
    TRY_CAST(year AS INTEGER)                       AS year,
    CAST(state AS VARCHAR)                          AS state,
    CAST(country AS VARCHAR)                        AS country,
    CAST(category AS VARCHAR)                       AS category,
    CAST(reading_type AS VARCHAR)                   AS reading_type,
    CAST(poll_id AS VARCHAR)                        AS poll_id,
    CAST(pollster AS VARCHAR)                       AS pollster,
    CAST(date_label AS VARCHAR)                     AS date_label,
    TRY_CAST(strptime(CAST(data_start_date AS VARCHAR), '%Y/%m/%d') AS DATE) AS poll_start_date,
    TRY_CAST(strptime(CAST(data_end_date   AS VARCHAR), '%Y/%m/%d') AS DATE) AS poll_end_date,
    TRY_CAST(regexp_extract(CAST(sample_size_raw AS VARCHAR), '[0-9]+') AS INTEGER) AS sample_size,
    NULLIF(regexp_extract(CAST(sample_size_raw AS VARCHAR), '[A-Za-z]+$'), '')      AS sample_population,
    TRY_CAST(margin_error AS DOUBLE)                AS margin_error,
    NULLIF(CAST(partisan AS VARCHAR), '')           AS partisan,
    CAST(candidate AS VARCHAR)                      AS candidate,
    CAST(affiliation AS VARCHAR)                    AS affiliation,
    TRY_CAST(value AS DOUBLE)                       AS value,
    CAST(spread_candidate AS VARCHAR)               AS spread_candidate,
    CAST(spread_value AS VARCHAR)                   AS spread_value,
    CAST(last_build_date AS VARCHAR)                AS last_build_date
FROM "realclearpolitics-poll-readings"
WHERE candidate IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
