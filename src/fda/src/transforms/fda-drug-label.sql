-- fda-drug-label: Structured Product Labeling (SPL) index: one row per current label document; openfda fields missing where no match (~67%).
SELECT
    "id" AS id,
    CAST(try_strptime("effective_time", '%Y%m%d') AS DATE) AS effective_time,
    NULLIF(trim("spl_set_id"), '') AS spl_set_id,
    NULLIF(trim("brand_name"), '') AS brand_name,
    NULLIF(trim("generic_name"), '') AS generic_name,
    NULLIF(trim("manufacturer_name"), '') AS manufacturer_name,
    NULLIF(trim("product_type"), '') AS product_type,
    NULLIF(trim("route"), '') AS route,
    NULLIF(trim("substance_name"), '') AS substance_name,
    NULLIF(trim("product_ndc"), '') AS product_ndc
FROM "fda-drug-label"
