SELECT
    CAST(county_id AS INTEGER)           AS country_id,
    country_code,
    country_name,
    CAST(country_ip5 AS INTEGER)         AS is_ip5,
    CAST(country_ue AS INTEGER)          AS is_eu,
    CAST(country_epo_member AS INTEGER)  AS is_epo_member,
    CAST(country_population AS BIGINT)   AS population
FROM "epo-countries"
