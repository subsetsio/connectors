-- fao-ea: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("donor_code" AS BIGINT)              AS donor_code,
    ltrim("donor_code_m49", '''')             AS donor_code_m49,
    "donor"                                   AS donor,
    CAST("recipient_country_code" AS BIGINT)  AS recipient_country_code,
    ltrim("recipient_country_code_m49", '''') AS recipient_country_code_m49,
    "recipient_country"                       AS recipient_country,
    CAST("item_code" AS BIGINT)               AS item_code,
    "item"                                    AS item,
    CAST("element_code" AS BIGINT)            AS element_code,
    "element"                                 AS element,
    CAST("purpose_code" AS BIGINT)            AS purpose_code,
    "purpose"                                 AS purpose,
    CAST("year" AS BIGINT)                    AS year,
    "unit"                                    AS unit,
    CAST("value" AS DOUBLE)                   AS value,
    "flag"                                    AS flag
FROM "fao-ea"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
