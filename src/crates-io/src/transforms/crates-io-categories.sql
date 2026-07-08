SELECT
    CAST(id AS BIGINT)                  AS id,
    slug,
    category,
    description,
    CAST(COALESCE(crates_cnt, '0') AS BIGINT) AS crates_cnt,
    path,
    CAST(created_at AS TIMESTAMP)       AS created_at
FROM "crates-io-categories"
WHERE id IS NOT NULL AND slug IS NOT NULL AND category IS NOT NULL
