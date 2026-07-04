-- fda-drug-shortages: Current and resolved drug shortages; a status log with no natural unique key (published keyless, exact duplicate source rows dropped). Dates arrive MM/DD/YYYY and are normalized to ISO by the fetch.
SELECT DISTINCT
    "package_ndc" AS package_ndc,
    "generic_name" AS generic_name,
    "company_name" AS company_name,
    "presentation" AS presentation,
    "status" AS status,
    "update_type" AS update_type,
    "therapeutic_category" AS therapeutic_category,
    NULLIF(trim("dosage_form"), '') AS dosage_form,
    TRY_CAST("initial_posting_date" AS DATE) AS initial_posting_date,
    TRY_CAST("update_date" AS DATE) AS update_date,
    TRY_CAST("discontinued_date" AS DATE) AS discontinued_date,
    "contact_info" AS contact_info,
    NULLIF(trim("related_info"), '') AS related_info
FROM "fda-drug-shortages"
