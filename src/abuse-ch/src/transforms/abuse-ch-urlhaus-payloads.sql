SELECT
    TRY_CAST(firstseen AS TIMESTAMP)    AS first_seen,
    url,
    filetype,
    md5,
    sha256,
    signature
FROM "abuse-ch-urlhaus-payloads"
WHERE sha256 IS NOT NULL
