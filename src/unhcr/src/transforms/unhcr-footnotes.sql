SELECT
    footnote,
    "year" AS period,
    CAST(coo_id AS BIGINT) AS origin_id,
    coo AS origin_name,
    coo_iso AS origin_iso3,
    CAST(coa_id AS BIGINT) AS asylum_country_id,
    coa AS asylum_country_name,
    coa_iso AS asylum_country_iso3,
    population_type
FROM "unhcr-footnotes"
