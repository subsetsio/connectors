SELECT
    identifier,
    transaction_type,
    CAST(date AS DATE)            AS date,
    CAST(value AS DOUBLE)         AS value,
    description,
    organisation_name,
    CAST(organisation_id AS BIGINT) AS organisation_id
FROM "itc-activity-transactions"
WHERE identifier IS NOT NULL
