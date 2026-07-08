SELECT
    TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER)            AS rank,
    title                     AS title,
    TRY_CAST(regexp_replace(lifetime_gross, '[^0-9]', '', 'g') AS BIGINT) AS lifetime_gross,
    TRY_CAST(regexp_replace(year, '[^0-9]', '', 'g') AS INTEGER)            AS release_year
FROM "box-office-mojo-top-lifetime-grosses"
WHERE TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER) IS NOT NULL
