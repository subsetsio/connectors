SELECT
    CAST(id AS INTEGER)               AS id,
    name_short,
    name_english,
    name,
    name_ascii,
    wikipedia,
    CAST(foundation_date AS DATE)     AS foundation_date,
    CAST(dissolution_date AS DATE)    AS dissolution_date,
    CAST(country_id AS INTEGER)       AS country_id,
    CAST(family_id AS INTEGER)        AS family_id
FROM "parlgov-data-party"
