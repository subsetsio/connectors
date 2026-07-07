SELECT
    CAST("year" AS BIGINT) AS year,
    CAST(coo_id AS BIGINT) AS origin_id,
    coo AS origin_code,
    coo_iso AS origin_iso3,
    trim(coo_name) AS origin_name,
    CAST(coa_id AS BIGINT) AS asylum_country_id,
    coa AS asylum_country_code,
    coa_iso AS asylum_country_iso3,
    trim(coa_name) AS asylum_country_name,
    CAST(total AS BIGINT) AS internally_displaced_persons
FROM "unhcr-idmc"
WHERE total IS NOT NULL
