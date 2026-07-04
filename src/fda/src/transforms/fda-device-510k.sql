-- fda-device-510k: 510(k) premarket notifications (device clearances).
SELECT
    "k_number" AS k_number,
    NULLIF(trim("applicant"), '') AS applicant,
    NULLIF(trim("device_name"), '') AS device_name,
    NULLIF(trim("product_code"), '') AS product_code,
    "clearance_type" AS clearance_type,
    "decision_code" AS decision_code,
    "decision_description" AS decision_description,
    TRY_CAST("decision_date" AS DATE) AS decision_date,
    TRY_CAST("date_received" AS DATE) AS date_received,
    NULLIF(trim("advisory_committee"), '') AS advisory_committee,
    "advisory_committee_description" AS advisory_committee_description,
    "review_advisory_committee" AS review_advisory_committee,
    NULLIF(trim("expedited_review_flag"), '') AS expedited_review_flag,
    "third_party_flag" AS third_party_flag,
    NULLIF(trim("city"), '') AS city,
    NULLIF(trim("state"), '') AS state,
    NULLIF(trim("country_code"), '') AS country_code,
    NULLIF(trim("postal_code"), '') AS postal_code
FROM "fda-device-510k"
