-- fao-rfm: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("reporter_country_code" AS BIGINT)  AS reporter_country_code,
    ltrim("reporter_country_code_m49", '''') AS reporter_country_code_m49,
    "reporter_countries"                     AS reporter_countries,
    CAST("partner_country_code" AS BIGINT)   AS partner_country_code,
    ltrim("partner_country_code_m49", '''')  AS partner_country_code_m49,
    "partner_countries"                      AS partner_countries,
    CAST("item_code" AS BIGINT)              AS item_code,
    ltrim("item_code_cpc", '''')             AS item_code_cpc,
    "item"                                   AS item,
    CAST("element_code" AS BIGINT)           AS element_code,
    "element"                                AS element,
    CAST("year" AS BIGINT)                   AS year,
    "unit"                                   AS unit,
    CAST("value" AS DOUBLE)                  AS value,
    "flag"                                   AS flag
FROM "fao-rfm"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
