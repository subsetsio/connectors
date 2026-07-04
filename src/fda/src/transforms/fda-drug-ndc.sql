-- fda-drug-ndc: NDC Directory: one row per marketed drug product (product_id = NDC + SPL doc id).
SELECT
    "product_id" AS product_id,
    "product_ndc" AS product_ndc,
    "spl_id" AS spl_id,
    NULLIF(trim("brand_name"), '') AS brand_name,
    NULLIF(trim("brand_name_base"), '') AS brand_name_base,
    "generic_name" AS generic_name,
    "labeler_name" AS labeler_name,
    "product_type" AS product_type,
    "dosage_form" AS dosage_form,
    "marketing_category" AS marketing_category,
    NULLIF(trim("application_number"), '') AS application_number,
    CAST(try_strptime("marketing_start_date", '%Y%m%d') AS DATE) AS marketing_start_date,
    CAST(try_strptime("listing_expiration_date", '%Y%m%d') AS DATE) AS listing_expiration_date,
    TRY_CAST("finished" AS BOOLEAN) AS finished
FROM "fda-drug-ndc"
