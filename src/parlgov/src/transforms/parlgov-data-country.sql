SELECT
    CAST(id AS INTEGER)               AS id,
    name                              AS country_name,
    name_short                        AS country_name_short,
    code_iso2,
    CAST(eu_accession_date AS DATE)   AS eu_accession_date,
    CAST(oecd_accession_date AS DATE) AS oecd_accession_date
FROM "parlgov-data-country"
