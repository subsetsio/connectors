SELECT
    CAST(id AS BIGINT) AS id,
    keyword,
    CAST(COALESCE(crates_cnt, '0') AS BIGINT) AS crates_cnt,
    CAST(created_at AS TIMESTAMP) AS created_at
FROM "crates-io-keywords"
WHERE id IS NOT NULL AND keyword IS NOT NULL
