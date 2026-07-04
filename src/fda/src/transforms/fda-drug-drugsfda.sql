-- fda-drug-drugsfda: Drugs@FDA approved drug applications; openfda-derived fields are first-listed values and missing where no openFDA match exists (~57%).
SELECT
    "application_number" AS application_number,
    "sponsor_name" AS sponsor_name,
    NULLIF(trim("brand_name"), '') AS brand_name,
    NULLIF(trim("generic_name"), '') AS generic_name,
    NULLIF(trim("manufacturer_name"), '') AS manufacturer_name,
    NULLIF(trim("product_type"), '') AS product_type,
    NULLIF(trim("route"), '') AS route,
    NULLIF(trim("substance_name"), '') AS substance_name
FROM "fda-drug-drugsfda"
