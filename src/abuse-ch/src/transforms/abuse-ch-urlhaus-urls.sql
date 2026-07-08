SELECT
    TRY_CAST(id AS BIGINT)              AS id,
    TRY_CAST(dateadded AS TIMESTAMP)    AS date_added,
    url,
    url_status,
    TRY_CAST(last_online AS TIMESTAMP)  AS last_online,
    threat,
    tags,
    urlhaus_link,
    reporter
FROM "abuse-ch-urlhaus-urls"
WHERE url IS NOT NULL
