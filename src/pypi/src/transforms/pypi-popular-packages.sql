SELECT
    package,
    CAST(rank AS INTEGER)               AS rank,
    CAST(download_count_30d AS BIGINT)  AS download_count_30d,
    version,
    summary,
    author,
    author_email,
    license,
    requires_python,
    home_page,
    keywords,
    CAST(yanked AS BOOLEAN)             AS yanked
FROM "pypi-popular-packages"
WHERE package IS NOT NULL
