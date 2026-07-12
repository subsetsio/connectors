SELECT
    CAST(crate_id AS BIGINT) AS crate_id,
    CAST(keyword_id AS BIGINT) AS keyword_id
FROM "crates-io-crate-keywords"
WHERE crate_id IS NOT NULL AND keyword_id IS NOT NULL
