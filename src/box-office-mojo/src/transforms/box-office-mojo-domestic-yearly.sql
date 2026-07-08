SELECT
    CAST(year AS INTEGER)   AS year,
    TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER)          AS rank,
    release                 AS release,
    TRY_CAST(regexp_replace(gross, '[^0-9]', '', 'g') AS BIGINT)       AS gross,
    TRY_CAST(regexp_replace(theaters, '[^0-9]', '', 'g') AS INTEGER)      AS theaters,
    TRY_CAST(regexp_replace(total_gross, '[^0-9]', '', 'g') AS BIGINT) AS total_gross,
    NULLIF(release_date, '-') AS release_date,
    NULLIF(distributor, '-')  AS distributor,
    NULLIF(genre, '-')        AS genre,
    (estimated = 'True')    AS estimated
FROM "box-office-mojo-domestic-yearly"
WHERE TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER) IS NOT NULL
