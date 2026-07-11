SELECT
    CAST(id AS BIGINT)         AS id,
    CAST(parent_id AS BIGINT)  AS parent_id,
    code,
    name,
    description,
    color,
    CAST(vocabulary AS BIGINT) AS vocabulary
FROM "itc-vocabulary-codes"
WHERE id IS NOT NULL
