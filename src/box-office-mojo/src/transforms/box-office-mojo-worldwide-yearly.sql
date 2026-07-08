SELECT
    CAST(year AS INTEGER)    AS year,
    TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER)           AS rank,
    release_group            AS release_group,
    TRY_CAST(regexp_replace(worldwide, '[^0-9]', '', 'g') AS BIGINT)    AS worldwide_gross,
    TRY_CAST(regexp_replace(domestic, '[^0-9]', '', 'g') AS BIGINT)     AS domestic_gross,
    TRY_CAST(regexp_replace(domestic_pct, '[^0-9.-]', '', 'g') AS DOUBLE)   AS domestic_pct,
    TRY_CAST(regexp_replace("foreign", '[^0-9]', '', 'g') AS BIGINT)    AS foreign_gross,
    TRY_CAST(regexp_replace(foreign_pct, '[^0-9.-]', '', 'g') AS DOUBLE)    AS foreign_pct
FROM "box-office-mojo-worldwide-yearly"
WHERE TRY_CAST(regexp_replace(rank, '[^0-9]', '', 'g') AS INTEGER) IS NOT NULL
