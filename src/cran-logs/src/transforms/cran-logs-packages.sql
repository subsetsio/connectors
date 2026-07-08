SELECT
    package,
    version,
    title,
    description,
    license,
    maintainer,
    needs_compilation,
    TRY_CAST(date_publication AS TIMESTAMP) AS date_publication,
    url,
    bugreports,
    repository
FROM "cran-logs-packages"
WHERE package IS NOT NULL
