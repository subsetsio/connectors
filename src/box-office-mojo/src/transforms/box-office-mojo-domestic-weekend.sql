SELECT
    weekend_id               AS weekend_id,
    CAST(year AS INTEGER)    AS year,
    TRY_CAST(regexp_replace(week, '[^0-9]', '', 'g') AS INTEGER)           AS week,
    TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER)           AS rank,
    TRY_CAST(regexp_replace(last_week_rank, '[^0-9]', '', 'g') AS INTEGER) AS last_week_rank,
    release                  AS release,
    TRY_CAST(regexp_replace(gross, '[^0-9]', '', 'g') AS BIGINT)        AS gross,
    TRY_CAST(regexp_replace(weekend_change_pct, '[^0-9.-]', '', 'g') AS DOUBLE) AS weekend_change_pct,
    TRY_CAST(regexp_replace(theaters, '[^0-9]', '', 'g') AS INTEGER)       AS theaters,
    TRY_CAST(regexp_replace(theater_change, '[^0-9-]', '', 'g') AS INTEGER) AS theater_change,
    TRY_CAST(regexp_replace(average, '[^0-9]', '', 'g') AS BIGINT)      AS average_per_theater,
    TRY_CAST(regexp_replace(total_gross, '[^0-9]', '', 'g') AS BIGINT)  AS total_gross,
    TRY_CAST(regexp_replace(weeks, '[^0-9]', '', 'g') AS INTEGER)          AS weeks_in_release,
    NULLIF(distributor, '-') AS distributor,
    (new_this_week = 'True') AS new_this_week,
    (estimated = 'True')     AS estimated
FROM "box-office-mojo-domestic-weekend"
WHERE TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER) IS NOT NULL
