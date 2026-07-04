-- fda-other-nsde: Comprehensive NDC SPL Data Elements (NSDE): one row per package NDC.
SELECT
    "package_ndc" AS package_ndc,
    "package_ndc11" AS package_ndc11,
    NULLIF(trim("proprietary_name"), '') AS proprietary_name,
    NULLIF(trim("dosage_form"), '') AS dosage_form,
    "marketing_category" AS marketing_category,
    NULLIF(trim("application_number_or_citation"), '') AS application_number_or_citation,
    trim("product_type") AS product_type,
    NULLIF(trim("billing_unit"), '') AS billing_unit,
    CAST(try_strptime("marketing_start_date", '%Y%m%d') AS DATE) AS marketing_start_date,
    CAST(try_strptime("marketing_end_date", '%Y%m%d') AS DATE) AS marketing_end_date,
    CAST(try_strptime("inactivation_date", '%Y%m%d') AS DATE) AS inactivation_date,
    CAST(try_strptime("reactivation_date", '%Y%m%d') AS DATE) AS reactivation_date
FROM "fda-other-nsde"
