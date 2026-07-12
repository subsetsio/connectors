SELECT
    CAST(crate_id AS BIGINT) AS crate_id,
    CAST(category_id AS BIGINT) AS category_id
FROM "crates-io-crate-categories"
WHERE crate_id IS NOT NULL AND category_id IS NOT NULL
