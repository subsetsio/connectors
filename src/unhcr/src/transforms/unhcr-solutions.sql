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
    CAST(returned_refugees AS BIGINT) AS returned_refugees,
    CAST(resettlement AS BIGINT) AS resettled_refugees,
    CAST(naturalisation AS BIGINT) AS naturalized_persons,
    CAST(returned_idps AS BIGINT) AS returned_internally_displaced_persons
FROM "unhcr-solutions"
WHERE returned_refugees IS NOT NULL
   OR resettlement IS NOT NULL
   OR naturalisation IS NOT NULL
   OR returned_idps IS NOT NULL
