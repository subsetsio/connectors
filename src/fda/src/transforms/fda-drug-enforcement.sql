-- fda-drug-enforcement: Weekly FDA Enforcement Report recalls, drugs only (constant product_type dropped).
SELECT
    "recall_number" AS recall_number,
    TRY_CAST(TRY_CAST("event_id" AS DOUBLE) AS BIGINT) AS event_id,
    "status" AS status,
    "classification" AS classification,
    "recalling_firm" AS recalling_firm,
    NULLIF(trim("product_description"), '') AS product_description,
    NULLIF(trim("product_quantity"), '') AS product_quantity,
    NULLIF(trim("reason_for_recall"), '') AS reason_for_recall,
    NULLIF(trim("voluntary_mandated"), '') AS voluntary_mandated,
    NULLIF(trim("initial_firm_notification"), '') AS initial_firm_notification,
    NULLIF(trim("distribution_pattern"), '') AS distribution_pattern,
    CAST(try_strptime("recall_initiation_date", '%Y%m%d') AS DATE) AS recall_initiation_date,
    CAST(try_strptime("center_classification_date", '%Y%m%d') AS DATE) AS center_classification_date,
    CAST(try_strptime("report_date", '%Y%m%d') AS DATE) AS report_date,
    CAST(try_strptime("termination_date", '%Y%m%d') AS DATE) AS termination_date,
    NULLIF(trim("city"), '') AS city,
    NULLIF(trim("state"), '') AS state,
    NULLIF(trim("country"), '') AS country,
    NULLIF(trim("postal_code"), '') AS postal_code
FROM "fda-drug-enforcement"
