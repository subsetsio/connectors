-- fda-device-recall: Device recalls from the FDA Recall Enterprise System (RES).
SELECT
    "product_res_number" AS product_res_number,
    TRY_CAST(TRY_CAST("cfres_id" AS DOUBLE) AS BIGINT) AS cfres_id,
    TRY_CAST(TRY_CAST("res_event_number" AS DOUBLE) AS BIGINT) AS res_event_number,
    "recall_status" AS recall_status,
    NULLIF(trim("action"), '') AS action,
    NULLIF(trim("product_code"), '') AS product_code,
    NULLIF(trim("product_description"), '') AS product_description,
    NULLIF(trim("product_quantity"), '') AS product_quantity,
    "recalling_firm" AS recalling_firm,
    NULLIF(trim("reason_for_recall"), '') AS reason_for_recall,
    "root_cause_description" AS root_cause_description,
    NULLIF(trim("distribution_pattern"), '') AS distribution_pattern,
    TRY_CAST(TRY_CAST("firm_fei_number" AS DOUBLE) AS BIGINT) AS firm_fei_number,
    TRY_CAST("event_date_created" AS DATE) AS event_date_created,
    TRY_CAST("event_date_initiated" AS DATE) AS event_date_initiated,
    TRY_CAST("event_date_posted" AS DATE) AS event_date_posted,
    TRY_CAST("event_date_terminated" AS DATE) AS event_date_terminated,
    "city" AS city,
    "state" AS state,
    "postal_code" AS postal_code
FROM "fda-device-recall"
