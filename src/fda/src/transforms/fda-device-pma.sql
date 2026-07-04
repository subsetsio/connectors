-- fda-device-pma: Premarket approvals: one row per PMA original or supplement.
SELECT
    "pma_number" AS pma_number,
    "supplement_number" AS supplement_number,
    NULLIF(trim("supplement_type"), '') AS supplement_type,
    NULLIF(trim("supplement_reason"), '') AS supplement_reason,
    "applicant" AS applicant,
    "trade_name" AS trade_name,
    NULLIF(trim("generic_name"), '') AS generic_name,
    NULLIF(trim("product_code"), '') AS product_code,
    "advisory_committee" AS advisory_committee,
    "advisory_committee_description" AS advisory_committee_description,
    "decision_code" AS decision_code,
    TRY_CAST("decision_date" AS DATE) AS decision_date,
    TRY_CAST("date_received" AS DATE) AS date_received,
    TRY_CAST("fed_reg_notice_date" AS DATE) AS fed_reg_notice_date,
    "expedited_review_flag" AS expedited_review_flag,
    NULLIF(trim("docket_number"), '') AS docket_number,
    NULLIF(trim("city"), '') AS city,
    NULLIF(trim("state"), '') AS state
FROM "fda-device-pma"
